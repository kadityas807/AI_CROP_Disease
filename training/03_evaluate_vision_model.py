"""Evaluate the saved vision checkpoint on its matching validation split."""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import torch
from torch.utils.data import DataLoader
from torchvision import datasets

from backend.ml_engine.vision_classifier import vision_classifier


DEFAULT_VALIDATION_DIR = PROJECT_ROOT / "data" / "processed" / "PlantVillage_Split" / "val"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "reports" / "vision_validation_metrics.json"


def evaluate(validation_dir: Path, batch_size: int) -> dict:
    if not validation_dir.is_dir():
        raise FileNotFoundError(f"Validation images were not found: {validation_dir}")

    dataset = datasets.ImageFolder(
        str(validation_dir),
        transform=vision_classifier.transform,
    )
    if dataset.classes != vision_classifier.classes:
        raise ValueError(
            "Validation class folders do not exactly match models/vision_classes.txt. "
            "Use the validation split corresponding to this checkpoint."
        )
    if len(dataset) == 0:
        raise ValueError(f"No validation images were found in {validation_dir}")

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
    )
    class_count = len(dataset.classes)
    confusion = torch.zeros((class_count, class_count), dtype=torch.int64)
    top3_correct = 0
    top5_correct = 0
    total = 0
    started_at = time.monotonic()
    print(
        f"Evaluating {len(dataset)} validation images across {class_count} classes...",
        flush=True,
    )

    vision_classifier.model.eval()
    with torch.inference_mode():
        for batch_index, (images, labels) in enumerate(loader, start=1):
            outputs = vision_classifier.model(images.to(vision_classifier.device))
            labels = labels.to(vision_classifier.device)
            predictions = outputs.argmax(dim=1)
            counts = torch.bincount(
                labels.cpu() * class_count + predictions.cpu(),
                minlength=class_count * class_count,
            )
            confusion += counts.reshape(class_count, class_count)
            top_indices = outputs.topk(min(5, class_count), dim=1).indices
            top3_correct += (top_indices[:, :min(3, class_count)] == labels[:, None]).any(dim=1).sum().item()
            top5_correct += (top_indices == labels[:, None]).any(dim=1).sum().item()
            total += labels.numel()
            if batch_index % 50 == 0 or total == len(dataset):
                print(
                    f"Processed {total}/{len(dataset)} images "
                    f"({time.monotonic() - started_at:.0f}s elapsed)",
                    flush=True,
                )

    true_positive = confusion.diag().double()
    support = confusion.sum(dim=1).double()
    predicted = confusion.sum(dim=0).double()
    precision = true_positive / predicted.clamp_min(1)
    recall = true_positive / support.clamp_min(1)
    f1 = 2 * precision * recall / (precision + recall).clamp_min(1e-12)
    accuracy = true_positive.sum().item() / total

    return {
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
        "checkpoint": str(vision_classifier.model_path),
        "validation_directory": str(validation_dir.resolve()),
        "evaluation_split_note": (
            "Validation metrics only. The training pipeline uses this split for model "
            "selection, so these are not an independent final test-set estimate."
        ),
        "sample_count": total,
        "class_count": class_count,
        "accuracy": round(accuracy, 6),
        "top_3_accuracy": round(top3_correct / total, 6),
        "top_5_accuracy": round(top5_correct / total, 6),
        "macro_precision": round(precision.mean().item(), 6),
        "macro_recall": round(recall.mean().item(), 6),
        "macro_f1": round(f1.mean().item(), 6),
        "weighted_f1": round((f1 * support).sum().item() / support.sum().item(), 6),
        "per_class": [
            {
                "class_name": class_name,
                "support": int(support[index].item()),
                "precision": round(precision[index].item(), 6),
                "recall": round(recall[index].item(), 6),
                "f1": round(f1[index].item(), 6),
            }
            for index, class_name in enumerate(dataset.classes)
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validation-dir",
        type=Path,
        default=DEFAULT_VALIDATION_DIR,
        help="Validation directory whose class folders match the saved checkpoint.",
    )
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help="Path for the JSON metrics report.",
    )
    args = parser.parse_args()
    if args.batch_size < 1:
        parser.error("--batch-size must be at least 1")

    report = evaluate(args.validation_dir, args.batch_size)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Validation samples: {report['sample_count']}")
    print(f"Classes: {report['class_count']}")
    print(f"Accuracy: {report['accuracy']:.4%}")
    print(f"Macro F1: {report['macro_f1']:.4f}")
    print(f"Weighted F1: {report['weighted_f1']:.4f}")
    print(f"Top-3 accuracy: {report['top_3_accuracy']:.4%}")
    print(f"Report saved to {args.output.resolve()}")
    print(report["evaluation_split_note"])


if __name__ == "__main__":
    main()
