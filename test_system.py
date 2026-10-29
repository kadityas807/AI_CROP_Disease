"""Tests for image inference, environmental scoring, and metadata alignment."""

import io
from unittest.mock import patch
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from backend.main import app
from backend.ml_engine.environmental_risk import env_risk_engine
from backend.ml_engine.fusion_engine import MultimodalFusionEngine
from backend.ml_engine.vision_classifier import vision_classifier


client = TestClient(app)


def make_test_image():
    project_root = Path(__file__).parent
    source_dirs = [
        project_root / "data" / "raw" / "temp_plantvillage-dataset" /
        "plantvillage dataset" / "color" / "Tomato___healthy",
        project_root / "data" / "raw" / "PlantVillage" / "Tomato___healthy",
    ]
    for source_dir in source_dirs:
        if source_dir.is_dir():
            samples = [
                path for path in source_dir.iterdir()
                if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
            ]
            if samples:
                return samples[0].read_bytes()

    image = Image.new("RGB", (256, 256), color=(55, 120, 45))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_frontend_is_served():
    page = client.get("/")
    script = client.get("/static/js/app.js")
    assert page.status_code == 200
    assert "image capture date" in page.text.lower()
    assert "ask a crop question" in page.text.lower()
    assert script.status_code == 200


def test_crop_chatbot_answers_project_workflow_without_external_service():
    response = client.post(
        "/api/chat",
        json={"message": "How does this project work?"},
    )
    assert response.status_code == 200
    result = response.json()
    assert "MobileNetV2" in result["answer"]
    assert result["assistant"] == "Local crop knowledge assistant"


def test_crop_chatbot_uses_latest_prediction_for_symptoms():
    response = client.post(
        "/api/chat",
        json={
            "message": "What symptoms should I check?",
            "predicted_class": "Tomato___Late_blight",
        },
    )
    assert response.status_code == 200
    assert "Tomato Late Blight" in response.json()["answer"]
    assert "water-soaked" in response.json()["answer"]


def test_crop_chatbot_rejects_invalid_messages():
    empty = client.post("/api/chat", json={"message": ""})
    too_long = client.post("/api/chat", json={"message": "x" * 501})
    assert empty.status_code == 422
    assert too_long.status_code == 422


def test_model_loads_and_returns_predictions():
    result = vision_classifier.predict(make_test_image(), crop_hint="Tomato")
    assert result["engine"] == "PyTorch MobileNetV2"
    assert result["predicted_class"].startswith("Tomato")
    assert 0 <= result["confidence"] <= 1
    assert result["top_k"]


def test_all_plantvillage_crop_choices_have_model_classes():
    crops = [
        "Tomato", "Potato", "Corn (Maize)", "Apple", "Grape", "Bell Pepper",
        "Blueberry", "Cherry", "Orange", "Peach", "Raspberry", "Soybean",
        "Squash", "Strawberry",
    ]
    model_classes = set(vision_classifier.classes)
    for crop in crops:
        assert vision_classifier._crop_candidates(crop) & model_classes


def test_invalid_image_is_rejected():
    response = client.post(
        "/api/predict/image",
        files={"file": ("not-an-image.txt", b"not an image", "text/plain")},
    )
    assert response.status_code == 400


def test_environmental_rule_index_is_bounded_and_uses_weather_inputs():
    high = env_risk_engine.compute_disease_vulnerability(
        temperature=22.0,
        relative_humidity=95.0,
        rainfall_mm=30.0,
        leaf_wetness_hours=12.0,
    )
    low = env_risk_engine.compute_disease_vulnerability(
        temperature=35.0,
        relative_humidity=30.0,
        rainfall_mm=0.0,
        leaf_wetness_hours=1.0,
    )
    assert 0 <= low["composite_risk_score"] < high["composite_risk_score"] <= 100


def test_manual_weather_is_labeled_as_unaligned_simulation():
    response = client.post(
        "/api/predict/environmental",
        json={
            "temperature": 23.5,
            "relative_humidity": 88,
            "rainfall_mm": 15,
            "leaf_wetness_hours": 8,
        },
    )
    assert response.status_code == 200
    source = response.json()["data_source"]
    assert source["name"] == "User-entered controlled simulation"
    assert source["spatially_aligned"] is False
    assert source["temporally_aligned"] is False


def test_public_weather_metadata_is_required_together():
    response = client.post(
        "/api/predict/environmental",
        json={
            "temperature": 23.5,
            "relative_humidity": 88,
            "latitude": 30.9,
        },
    )
    assert response.status_code == 422


def test_invalid_observation_date_is_rejected_as_input():
    response = client.post(
        "/api/predict/environmental",
        json={
            "temperature": 23.5,
            "relative_humidity": 88,
            "latitude": 30.9,
            "longitude": 75.86,
            "observation_date": "not-a-date",
        },
    )
    assert response.status_code == 422


def test_fused_prediction_uses_aligned_public_weather():
    weather = {
        "temperature": 19.0,
        "relative_humidity": 91.0,
        "rainfall_mm": 7.5,
        "wind_speed_kmh": 12.0,
        "leaf_wetness_hours": 9.0,
        "source": {
            "name": "Open-Meteo Historical Weather API",
            "latitude": 30.9,
            "longitude": 75.86,
            "observation_date": "2025-08-18",
            "spatially_aligned": True,
            "temporally_aligned": True,
        },
    }
    with patch(
        "backend.api.routes.fetch_weather_for_observation",
        return_value=weather,
    ):
        response = client.post(
            "/api/predict/fused",
            data={
                "temperature": 23.5,
                "relative_humidity": 88,
                "rainfall_mm": 15,
                "leaf_wetness_hours": 8,
                "target_crop": "Tomato",
                "latitude": 30.9,
                "longitude": 75.86,
                "observation_date": "2025-08-18",
            },
            files={"file": ("leaf.png", make_test_image(), "image/png")},
        )
    assert response.status_code == 200
    result = response.json()
    source = result["environmental_details"]["data_source"]
    assert source["spatially_aligned"] is True
    assert source["temporally_aligned"] is True
    assert result["environmental_details"]["parameters"]["temperature"] == 19.0


def test_fused_prediction_requires_an_uploaded_image():
    response = client.post("/api/predict/fused", data={"target_crop": "Tomato"})
    assert response.status_code == 422


def test_sample_leaves_endpoint_returns_catalog():
    response = client.get("/api/samples/leaves")
    assert response.status_code == 200
    samples = response.json()
    assert len(samples) >= 4
    crops = {s["crop"] for s in samples}
    assert "Tomato" in crops
    assert "Potato" in crops


def test_fusion_transparency_weights_and_contributions():
    response = client.post(
        "/api/predict/fused",
        data={
            "temperature": 24.0,
            "relative_humidity": 90.0,
            "rainfall_mm": 20.0,
            "leaf_wetness_hours": 10.0,
            "target_crop": "Tomato",
        },
        files={"file": ("leaf.png", make_test_image(), "image/png")},
    )
    assert response.status_code == 200
    result = response.json()
    fusion = result["multimodal_fusion"]
    assert "vision_contribution" in fusion
    assert "environment_contribution" in fusion
    assert "fusion_weights" in fusion
    assert fusion["fusion_weights"]["W_VISION"] == 0.65
    assert fusion["fusion_weights"]["W_ENV"] == 0.35
    assert result["environmental_details"]["weather_source"] == "simulated"


def test_fusion_reasoning_labels_simulated_weather_and_limits_its_claims():
    engine = MultimodalFusionEngine()
    vision_result = {
        "predicted_class": "Tomato___Late_blight",
        "confidence": 0.7,
        "percentage": 70.0,
        "is_healthy": False,
    }
    environmental_result = {
        "composite_risk_score": 78.0,
        "parameters": {"temperature": 23.5, "relative_humidity": 92.0},
        "data_source": {
            "spatially_aligned": False,
            "temporally_aligned": False,
        },
    }

    simulated_result = engine.fuse(vision_result, environmental_result)
    simulated_reasons = " ".join(simulated_result["reasoning_summary"]).lower()
    assert "simulated humidity and wetness inputs" in simulated_reasons
    assert "not observed farm conditions" in simulated_reasons
    assert "does not increase confidence in the image match" in simulated_reasons
    assert "current humidity" not in simulated_reasons
    assert "simulated inputs only" in simulated_result["pathogen_weather_match"].lower()

    environmental_result["data_source"] = {
        "spatially_aligned": True,
        "temporally_aligned": True,
    }
    aligned_result = engine.fuse(vision_result, environmental_result)
    aligned_reasons = " ".join(aligned_result["reasoning_summary"]).lower()
    assert "observed humidity and wetness" in aligned_reasons
    assert "observed weather fits this disease profile" in aligned_reasons
    assert "not confirmation of the image match" in aligned_reasons


def test_low_confidence_rejection_for_ambiguous_image():
    import numpy as np
    from PIL import Image

    np.random.seed(42)
    noise = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
    img = Image.fromarray(noise)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")

    res = vision_classifier.predict(buf.getvalue(), crop_hint="Tomato")
    assert res["confidence_status"] == "low_confidence"
    assert res["low_confidence_message"] is not None




def test_canonical_class_mapping_and_probability_aggregation():
    from backend.ml_engine.vision_classifier import RAW_TO_CANONICAL
    assert RAW_TO_CANONICAL["Tomato_Early_blight"] == "Tomato___Early_blight"
    assert RAW_TO_CANONICAL["Pepper__bell___Bacterial_spot"] == "Pepper,_bell___Bacterial_spot"
    assert RAW_TO_CANONICAL["Bacterial leaf blight"] == "Rice___Bacterial_leaf_blight"
    assert len(vision_classifier.canonical_classes) == 41

    # Test that early blight image with crop_hint=None succeeds without false low-confidence rejection
    sample_path = Path(__file__).parent / "frontend" / "samples" / "tomato_early_blight.jpg"
    if sample_path.is_file():
        res = vision_classifier.predict(sample_path.read_bytes(), crop_hint=None)
        assert res["predicted_class"] == "Tomato___Early_blight"
        assert res["confidence_status"] == "ok"
        assert res["confidence"] > 0.80


def test_knowledge_base_covers_all_canonical_classes():
    from backend.database.knowledge_base import get_disease_profile
    for canon in vision_classifier.canonical_classes:
        prof = get_disease_profile(canon)
        assert prof["crop"], f"Missing crop for {canon}"
        assert prof["pathogen_type"], f"Missing pathogen_type for {canon}"
        assert prof["common_name"], f"Missing common_name for {canon}"


def test_healthy_plant_guidance_has_no_chemicals():
    from backend.database.knowledge_base import get_disease_profile
    healthy_classes = [c for c in vision_classifier.canonical_classes if "healthy" in c.lower()]
    assert len(healthy_classes) >= 12
    for h in healthy_classes:
        prof = get_disease_profile(h)
        assert prof["pathogen_type"] == "None"
        assert len(prof["management"]["chemical_controls"]) == 0
        assert len(prof["management"]["organic_controls"]) == 0


def test_bacterial_and_viral_safety_no_mancozeb():
    from backend.database.knowledge_base import get_disease_profile
    check_classes = [
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Tomato___Tomato_mosaic_virus",
        "Tomato___Bacterial_spot",
        "Pepper,_bell___Bacterial_spot",
        "Orange___Haunglongbing_(Citrus_greening)",
    ]
    for c in check_classes:
        prof = get_disease_profile(c)
        for chem in prof["management"]["chemical_controls"]:
            assert "mancozeb" not in chem["name"].lower(), f"Unsafe fungicide in {c}: {chem}"


def test_unknown_disease_fallback_safety():
    from backend.database.knowledge_base import get_disease_profile
    prof = get_disease_profile("NonExistent_Fake_Disease_XYZ")
    assert prof["pathogen_type"] == "Uncertain / Unverified"
    assert len(prof["management"]["chemical_controls"]) == 0
    assert "laboratory or agronomist confirmation" in prof["management"]["cultural_practices"]


def test_history_database_and_endpoints():
    # Test GET history
    get_res = client.get("/api/history")
    assert get_res.status_code == 200
    assert isinstance(get_res.json(), list)

    # Test scan save via prediction
    post_res = client.post(
        "/api/predict/fused",
        data={"target_crop": "Tomato", "temperature": 23.5, "relative_humidity": 88.0},
        files={"file": ("leaf.png", make_test_image(), "image/png")},
    )
    assert post_res.status_code == 200
    assert "scan_id" in post_res.json()

    # Verify scan is in history
    history_after = client.get("/api/history").json()
    assert len(history_after) >= 1
    assert history_after[0]["crop"] == "Tomato"

    # Test DELETE history
    del_res = client.delete("/api/history")
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "success"


def test_cors_configuration_is_safe():
    from backend.main import app
    from starlette.middleware.cors import CORSMiddleware
    for middleware in app.user_middleware:
        if middleware.cls == CORSMiddleware:
            assert middleware.kwargs.get("allow_credentials") is False


if __name__ == "__main__":
    tests = [
        test_health_endpoint,
        test_frontend_is_served,
        test_crop_chatbot_answers_project_workflow_without_external_service,
        test_crop_chatbot_uses_latest_prediction_for_symptoms,
        test_crop_chatbot_rejects_invalid_messages,
        test_model_loads_and_returns_predictions,
        test_all_plantvillage_crop_choices_have_model_classes,
        test_invalid_image_is_rejected,
        test_environmental_rule_index_is_bounded_and_uses_weather_inputs,
        test_manual_weather_is_labeled_as_unaligned_simulation,
        test_public_weather_metadata_is_required_together,
        test_invalid_observation_date_is_rejected_as_input,
        test_fused_prediction_uses_aligned_public_weather,
        test_fused_prediction_requires_an_uploaded_image,
        test_sample_leaves_endpoint_returns_catalog,
        test_fusion_transparency_weights_and_contributions,
        test_fusion_reasoning_labels_simulated_weather_and_limits_its_claims,
        test_low_confidence_rejection_for_ambiguous_image,
        test_canonical_class_mapping_and_probability_aggregation,
        test_knowledge_base_covers_all_canonical_classes,
        test_healthy_plant_guidance_has_no_chemicals,
        test_bacterial_and_viral_safety_no_mancozeb,
        test_unknown_disease_fallback_safety,
        test_history_database_and_endpoints,
        test_cors_configuration_is_safe,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
