"""PlantVillage image classifier backed by the trained MobileNetV2 model."""

import io
from pathlib import Path

from PIL import Image, UnidentifiedImageError
import torch
import torch.nn as nn
from torchvision import models, transforms

from backend.database.knowledge_base import CROPS_DATABASE


class VisionClassifier:
    def __init__(self):
        project_root = Path(__file__).resolve().parents[2]
        model_path = project_root / "models" / "vision_mobilenetv2.pth"
        classes_path = project_root / "models" / "vision_classes.txt"
        if not model_path.is_file() or not classes_path.is_file():
            raise FileNotFoundError(
                "The trained PlantVillage model and models/vision_classes.txt are required. "
                "Run the vision training pipeline before starting the API."
            )

        self.model_path = model_path
        self.classes = [
            line.strip()
            for line in classes_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        if not self.classes or len(self.classes) != len(set(self.classes)):
            raise ValueError("The vision class mapping is empty or contains duplicate labels.")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])

        self.model = models.mobilenet_v2(weights=None)
        feature_count = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Linear(feature_count, len(self.classes))
        state_dict = torch.load(
            model_path, map_location=self.device, weights_only=True
        )
        self.model.load_state_dict(state_dict, strict=True)
        self.model.to(self.device)
        self.model.eval()

    def _crop_candidates(self, crop_hint: str | None) -> set[str] | None:
        if not crop_hint or crop_hint.lower() == "auto":
            return None

        for crop_name, crop_info in CROPS_DATABASE.items():
            if crop_name.lower() == crop_hint.strip().lower():
                return set(crop_info["diseases"])

        candidates = {
            class_name for class_name in self.classes
            if crop_hint.strip().lower() in class_name.lower()
        }
        if not candidates:
            raise ValueError(f"Unsupported crop selection: {crop_hint}")
        return candidates

    # P05-A: confidence thresholds (tune on validation data)
    CONF_MIN = 0.50      # minimum top-1 probability to be considered confident
    MARGIN_MIN = 0.15    # minimum gap between top-1 and top-2 probabilities

    def _estimate_plant_tissue_ratio(self, image: Image.Image) -> float:
        """Estimate percentage of pixels consistent with plant foliage (green, yellow, brown)."""
        import numpy as np
        hsv = np.array(image.convert("HSV"))
        h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
        # In PIL HSV: Hue is 0..255. Plant foliage spans ~14..105 with moderate saturation & value
        mask = (h >= 14) & (h <= 105) & (s >= 20) & (v >= 18)
        return float(np.mean(mask))

    def _decide(
        self,
        probs: list,
        raw_candidate_mass: float | None = None,
        plant_ratio: float | None = None,
    ) -> dict:
        """Return confidence status given a ranked list of (label, prob) tuples and OOD guards."""
        top1, top2 = probs[0], probs[1] if len(probs) > 1 else (probs[0][0], 0.0)
        top1_score = top1[1]
        top2_score = top2[1] if isinstance(top2[1], float) else top2[1]

        # 1. Non-plant / non-leaf photo rejection (faces, screens, walls, objects)
        if plant_ratio is not None and plant_ratio < 0.06:
            return {
                "status": "low_confidence",
                "message": "Image does not appear to be a plant leaf. Please upload a clear photo of an actual crop leaf in daylight.",
            }

        # 2. Raw unnormalized candidate mass check (prevents candidate renormalization from inflating OOD noise)
        if raw_candidate_mass is not None and raw_candidate_mass < 0.20:
            return {
                "status": "low_confidence",
                "message": "Low model certainty for this crop. Retake a clear, close photo of one leaf in daylight.",
            }

        # 3. Standard top-1 and margin checks
        low = top1_score < self.CONF_MIN or (top1_score - top2_score) < self.MARGIN_MIN
        return {
            "status": "low_confidence" if low else "ok",
            "message": (
                "Not confident. Retake a clear, close photo of one leaf in daylight."
            ) if low else None,
        }

    def predict(self, image_bytes: bytes, crop_hint: str | None = None) -> dict:
        try:
            with Image.open(io.BytesIO(image_bytes)) as source_image:
                image = source_image.convert("RGB")
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            raise ValueError(f"Uploaded file is not a readable image: {exc}") from exc

        # P05 image dimension guard: reject images larger than 25 megapixels
        if image.width * image.height > 25_000_000:
            raise ValueError(
                f"Image resolution {image.width}x{image.height} exceeds the 25 MP limit. "
                "Resize the image and try again."
            )

        plant_ratio = self._estimate_plant_tissue_ratio(image)

        tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            probabilities = torch.softmax(self.model(tensor)[0], dim=0)

        raw_candidate_mass = None
        candidates = self._crop_candidates(crop_hint)
        if candidates is not None:
            candidate_indices = [
                index for index, name in enumerate(self.classes)
                if name in candidates
            ]
            if not candidate_indices:
                raise ValueError(
                    f"The trained model has no classes for crop selection: {crop_hint}"
                )
            raw_candidate_mass = float(probabilities[candidate_indices].sum().item())
            candidate_probabilities = probabilities[candidate_indices]
            candidate_probabilities = candidate_probabilities / max(raw_candidate_mass, 1e-8)
            sorted_positions = torch.argsort(candidate_probabilities, descending=True)
            sorted_indices = [
                candidate_indices[position]
                for position in sorted_positions.tolist()
            ]
            ranked_probabilities = candidate_probabilities[sorted_positions]
        else:
            ranked_probabilities, sorted_indices = torch.sort(
                probabilities, descending=True
            )

        top_k = []
        for rank, index in enumerate(sorted_indices[:5]):
            class_name = self.classes[index]
            probability = float(ranked_probabilities[rank].item())
            top_k.append({
                "class_name": class_name,
                "display_name": class_name.replace("___", " - ").replace("_", " "),
                "confidence": round(probability, 4),
                "percentage": round(probability * 100, 1),
            })

        best = top_k[0]

        # P05-A: determine confidence status with OOD and foliage checks
        ranked_pairs = [(entry["class_name"], entry["confidence"]) for entry in top_k]
        conf_decision = self._decide(
            ranked_pairs,
            raw_candidate_mass=raw_candidate_mass,
            plant_ratio=plant_ratio,
        )

        return {
            "predicted_class": best["class_name"],
            "display_name": best["display_name"],
            "confidence": best["confidence"],
            "percentage": best["percentage"],
            "is_healthy": "healthy" in best["class_name"].lower(),
            "confidence_status": conf_decision["status"],           # "ok" or "low_confidence"
            "low_confidence_message": conf_decision["message"],     # None or retake string
            "top_k": top_k,
            "image_dimensions": {"width": image.width, "height": image.height},
            "engine": "PyTorch MobileNetV2",
        }


vision_classifier = VisionClassifier()

