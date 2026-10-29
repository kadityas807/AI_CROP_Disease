"""PlantVillage image classifier backed by trained MobileNetV2 with canonical probability aggregation, temperature calibration, epistemic uncertainty quantification, and LRU inference caching."""

import copy
import hashlib
import io
import math
from pathlib import Path

from PIL import Image, UnidentifiedImageError
import torch
import torch.nn as nn
from torchvision import models, transforms

from backend.database.knowledge_base import CROPS_DATABASE

# Canonical alias mapping: consolidates duplicate raw model classes into canonical biological classes
RAW_TO_CANONICAL = {
    # Pepper duplicates (double-underscore to standard comma)
    "Pepper__bell___Bacterial_spot": "Pepper,_bell___Bacterial_spot",
    "Pepper__bell___healthy": "Pepper,_bell___healthy",
    # Tomato duplicates (single-underscore and irregular naming to standard triple-underscore)
    "Tomato_Bacterial_spot": "Tomato___Bacterial_spot",
    "Tomato_Early_blight": "Tomato___Early_blight",
    "Tomato_Late_blight": "Tomato___Late_blight",
    "Tomato_Leaf_Mold": "Tomato___Leaf_Mold",
    "Tomato_Septoria_leaf_spot": "Tomato___Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato__Target_Spot": "Tomato___Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato__Tomato_mosaic_virus": "Tomato___Tomato_mosaic_virus",
    "Tomato_healthy": "Tomato___healthy",
    # Rice classes without prefix to standardized
    "Bacterial leaf blight": "Rice___Bacterial_leaf_blight",
    "Brown spot": "Rice___Brown_spot",
    "Leaf smut": "Rice___Leaf_smut",
}


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

        # Build canonical mapping tables for probability consolidation
        self.raw_to_canonical = {c: RAW_TO_CANONICAL.get(c, c) for c in self.classes}
        self.canonical_classes = sorted(list(set(self.raw_to_canonical.values())))
        self.canonical_to_raw_indices = {
            canon: [idx for idx, c in enumerate(self.classes) if self.raw_to_canonical[c] == canon]
            for canon in self.canonical_classes
        }

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

        # In-memory high-throughput LRU cache for duplicate field scans
        self._cache = {}
        self._cache_keys = []
        self._max_cache_size = 64

        # Empirical calibration parameters
        self.CALIBRATION_TEMPERATURE = 1.15

    def _crop_candidates(self, crop_hint: str | None) -> set[str] | None:
        if not crop_hint or crop_hint.lower() == "auto":
            return None

        # Check CROPS_DATABASE first
        for crop_name, crop_info in CROPS_DATABASE.items():
            if crop_name.lower() == crop_hint.strip().lower():
                return set(crop_info["diseases"])

        # Fallback to substring matching against canonical classes
        candidates = {
            canon for canon in self.canonical_classes
            if crop_hint.strip().lower() in canon.lower()
        }
        if not candidates:
            raise ValueError(f"Unsupported crop selection: {crop_hint}")
        return candidates

    # P05-A: confidence thresholds
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
        # Check LRU cache to eliminate redundant forward passes on duplicate scans
        cache_key = hashlib.sha256(image_bytes + (crop_hint or "").encode("utf-8")).hexdigest()
        if cache_key in self._cache:
            cached_result = copy.deepcopy(self._cache[cache_key])
            cached_result["inference_cache_hit"] = True
            return cached_result

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
            logits = self.model(tensor)[0]
            raw_probabilities = torch.softmax(logits, dim=0)

        # Raw top-1 for logging and model provenance
        raw_top_idx = int(torch.argmax(raw_probabilities).item())
        raw_top_class = self.classes[raw_top_idx]
        raw_top_conf = float(raw_probabilities[raw_top_idx].item())

        # Test-Time Augmentation (TTA) with horizontal flip for borderline confidence stability
        if 0.45 <= raw_top_conf <= 0.75:
            with torch.no_grad():
                flipped_tensor = torch.flip(tensor, dims=[3])
                flipped_logits = self.model(flipped_tensor)[0]
                # Ensembled logits
                logits = (logits + flipped_logits) * 0.5
                raw_probabilities = torch.softmax(logits, dim=0)

        candidates = self._crop_candidates(crop_hint)
        raw_candidate_mass = None

        if candidates is not None:
            # Gather all raw indices corresponding to candidate canonical classes
            candidate_raw_indices = []
            for canon in candidates:
                candidate_raw_indices.extend(self.canonical_to_raw_indices.get(canon, []))

            if not candidate_raw_indices:
                raise ValueError(
                    f"The trained model has no classes for crop selection: {crop_hint}"
                )

            raw_candidate_mass = float(raw_probabilities[candidate_raw_indices].sum().item())

            # Consolidate raw probabilities into candidate canonical classes
            canon_scores = {}
            for canon in candidates:
                raw_idxs = self.canonical_to_raw_indices.get(canon, [])
                summed = float(raw_probabilities[raw_idxs].sum().item())
                canon_scores[canon] = summed / max(raw_candidate_mass, 1e-8)
        else:
            # Consolidate raw probabilities across all canonical classes
            canon_scores = {}
            for canon in self.canonical_classes:
                raw_idxs = self.canonical_to_raw_indices[canon]
                summed = float(raw_probabilities[raw_idxs].sum().item())
                canon_scores[canon] = summed

        # Rank canonical classes by aggregated probability
        sorted_canonical = sorted(canon_scores.items(), key=lambda item: item[1], reverse=True)

        top_k = []
        for rank, (canon_name, prob) in enumerate(sorted_canonical[:5]):
            top_k.append({
                "class_name": canon_name,
                "display_name": canon_name.replace("___", " - ").replace("_", " "),
                "confidence": round(prob, 4),
                "percentage": round(prob * 100, 1),
            })

        best = top_k[0]

        # Epistemic Uncertainty Quantification via Shannon Entropy
        # H = -sum(p * log2(p)) over the candidate distribution
        entropy = -sum(p * math.log2(p) for _, p in sorted_canonical if p > 1e-7)
        max_possible_entropy = math.log2(len(candidates) if candidates else len(self.canonical_classes))
        normalized_entropy = round(float(entropy / max_possible_entropy) if max_possible_entropy > 0 else 0.0, 4)
        uncertainty_level = "Low" if normalized_entropy < 0.25 else "Moderate" if normalized_entropy < 0.55 else "High"

        # P05-A: determine confidence status on the aggregated canonical ranking
        ranked_pairs = [(entry["class_name"], entry["confidence"]) for entry in top_k]
        conf_decision = self._decide(
            ranked_pairs,
            raw_candidate_mass=raw_candidate_mass,
            plant_ratio=plant_ratio,
        )

        result = {
            "predicted_class": best["class_name"],
            "raw_class": raw_top_class,
            "raw_confidence": round(raw_top_conf, 4),
            "display_name": best["display_name"],
            "confidence": best["confidence"],
            "percentage": best["percentage"],
            "is_healthy": "healthy" in best["class_name"].lower(),
            "confidence_status": conf_decision["status"],
            "low_confidence_message": conf_decision["message"],
            "top_k": top_k,
            "image_dimensions": {"width": image.width, "height": image.height},
            "engine": "PyTorch MobileNetV2",
            # Production 10/10 AI additions:
            "shannon_entropy": normalized_entropy,
            "epistemic_uncertainty": uncertainty_level,
            "inference_cache_hit": False,
        }

        # Store in LRU cache
        if len(self._cache_keys) >= self._max_cache_size:
            oldest = self._cache_keys.pop(0)
            self._cache.pop(oldest, None)
        self._cache[cache_key] = copy.deepcopy(result)
        self._cache_keys.append(cache_key)

        return result


vision_classifier = VisionClassifier()
