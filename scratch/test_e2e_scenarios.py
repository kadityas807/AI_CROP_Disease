"""End-to-End Verification of 9 Core SIH Demonstration Scenarios."""
import io
import json
import sqlite3
import sys
from pathlib import Path
from unittest.mock import patch

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PIL import Image
from fastapi.testclient import TestClient

from backend.main import app
from backend.ml_engine.vision_classifier import vision_classifier, RAW_TO_CANONICAL
from backend.ml_engine.environmental_risk import env_risk_engine
from backend.ml_engine.fusion_engine import MultimodalFusionEngine
from backend.database.knowledge_base import get_disease_profile
from backend.database.db import crop_db

client = TestClient(app)

def create_sample_leaf():
    img = Image.new("RGB", (256, 256), color=(60, 130, 50))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

results = []

def run_scenario(name, fn):
    try:
        fn()
        results.append((name, "PASS", "Verified successfully"))
        print(f"[PASS] {name}")
    except Exception as e:
        results.append((name, "FAIL", str(e)))
        print(f"[FAIL] {name}: {e}")

# Scenario 1: Image inference pipeline
def s1():
    img_bytes = create_sample_leaf()
    res = vision_classifier.predict(img_bytes, crop_hint="Tomato")
    assert res["engine"] == "PyTorch MobileNetV2"
    assert res["predicted_class"].startswith("Tomato")
    assert 0 <= res["confidence"] <= 1.0
    assert len(res["top_k"]) > 0

# Scenario 2: Canonical 41-class aggregation
def s2():
    assert len(vision_classifier.canonical_classes) == 41
    # 53 raw classes are consolidated down to 41 canonical classes via RAW_TO_CANONICAL remapping
    assert len(RAW_TO_CANONICAL) == 15
    assert RAW_TO_CANONICAL["Tomato_Early_blight"] == "Tomato___Early_blight"
    assert RAW_TO_CANONICAL["Pepper__bell___Bacterial_spot"] == "Pepper,_bell___Bacterial_spot"
    assert RAW_TO_CANONICAL["Bacterial leaf blight"] == "Rice___Bacterial_leaf_blight"

# Scenario 3: Fused prediction with simulated weather
def s3():
    resp = client.post(
        "/api/predict/fused",
        data={
            "temperature": 24.5,
            "relative_humidity": 89.0,
            "rainfall_mm": 18.0,
            "leaf_wetness_hours": 9.0,
            "target_crop": "Tomato",
        },
        files={"file": ("leaf.jpg", create_sample_leaf(), "image/jpeg")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["environmental_details"]["weather_source"] == "simulated"
    assert data["multimodal_fusion"]["fusion_weights"]["W_VISION"] == 0.65
    assert data["multimodal_fusion"]["fusion_weights"]["W_ENV"] == 0.35
    assert any("simulated" in r.lower() for r in data["multimodal_fusion"]["reasoning_summary"])

# Scenario 4: Fused prediction with aligned Open-Meteo weather
def s4():
    mock_weather = {
        "temperature": 21.0,
        "relative_humidity": 92.0,
        "rainfall_mm": 10.0,
        "wind_speed_kmh": 8.0,
        "leaf_wetness_hours": 11.0,
        "source": {
            "name": "Open-Meteo Historical Weather API",
            "latitude": 30.90,
            "longitude": 75.86,
            "observation_date": "2025-08-15",
            "spatially_aligned": True,
            "temporally_aligned": True,
        },
    }
    with patch("backend.api.routes.fetch_weather_for_observation", return_value=mock_weather):
        resp = client.post(
            "/api/predict/fused",
            data={
                "temperature": 25.0,
                "relative_humidity": 80.0,
                "latitude": 30.90,
                "longitude": 75.86,
                "observation_date": "2025-08-15",
                "target_crop": "Tomato",
            },
            files={"file": ("leaf.jpg", create_sample_leaf(), "image/jpeg")},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["environmental_details"]["weather_source"] == "open-meteo"
        assert data["environmental_details"]["data_source"]["spatially_aligned"] is True

# Scenario 5: Low-confidence rejection / out-of-domain leaf
def s5():
    import numpy as np
    np.random.seed(123)
    noise = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
    img = Image.fromarray(noise)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    res = vision_classifier.predict(buf.getvalue(), crop_hint="Tomato")
    assert res["confidence_status"] == "low_confidence"
    assert res["low_confidence_message"] is not None

# Scenario 6: Knowledge base agricultural safety (ICAR/CIBRC standards)
def s6():
    # 1. Healthy plant has 0 chemicals
    healthy_profile = get_disease_profile("Tomato___healthy")
    assert len(healthy_profile["management"]["chemical_controls"]) == 0
    assert len(healthy_profile["management"]["organic_controls"]) == 0
    # 2. Viral disease has NO Mancozeb (fungicide)
    viral_profile = get_disease_profile("Tomato___Tomato_Yellow_Leaf_Curl_Virus")
    for chem in viral_profile["management"]["chemical_controls"]:
        assert "mancozeb" not in chem["name"].lower()
    # 3. Bacterial disease has NO Mancozeb
    bact_profile = get_disease_profile("Tomato___Bacterial_spot")
    for chem in bact_profile["management"]["chemical_controls"]:
        assert "mancozeb" not in chem["name"].lower()
    # 4. Fallback profile
    unknown_profile = get_disease_profile("FictionalCrop___FakeDisease")
    assert len(unknown_profile["management"]["chemical_controls"]) == 0

# Scenario 7: SQLite persistence lifecycle
def s7():
    crop_db.clear_history()
    scan_id = crop_db.save_scan(
        crop="Tomato",
        predicted_class="Tomato___Early_blight",
        disease_name="Early Blight",
        confidence=0.88,
        confidence_status="ok",
        risk_score=83.5,
        weather_source="simulated",
        temperature=24.5,
        humidity=89.0,
        rainfall=18.0,
        image_bytes=b"dummy_image_data"
    )
    assert scan_id > 0
    history = crop_db.get_recent_scans()
    assert len(history) == 1
    assert history[0]["crop"] == "Tomato"
    assert history[0]["predicted_class"] == "Tomato___Early_blight"
    crop_db.clear_history()
    assert len(crop_db.get_recent_scans()) == 0

# Scenario 8: Local Crop Assistant AI chatbot
def s8():
    resp1 = client.post("/api/chat", json={"message": "How does this project work?"})
    assert resp1.status_code == 200
    assert "MobileNetV2" in resp1.json()["answer"]

    resp2 = client.post("/api/chat", json={"message": "What symptoms should I check?", "predicted_class": "Tomato___Late_blight"})
    assert resp2.status_code == 200
    assert "water-soaked" in resp2.json()["answer"]

    resp_invalid = client.post("/api/chat", json={"message": ""})
    assert resp_invalid.status_code == 422

# Scenario 9: Multilingual UI & Accessibility integrity
def s9():
    with open(PROJECT_ROOT / "frontend" / "index.html", "r", encoding="utf-8") as f:
        html = f.read()
    with open(PROJECT_ROOT / "frontend" / "js" / "app.js", "r", encoding="utf-8") as f:
        js = f.read()
    assert "data-i18n=\"hero_title\"" in html
    assert "data-i18n=\"btn_check_leaf\"" in html
    assert "btn_camera" in js
    assert "hero_history_btn" in js
    # Confirm bilingual dicts
    assert "TRANSLATIONS = {" in js
    assert "en: {" in js
    assert "hi: {" in js
    assert "कैमरा" in js

if __name__ == "__main__":
    run_scenario("Scenario 1: Image inference pipeline", s1)
    run_scenario("Scenario 2: Canonical 41-class aggregation", s2)
    run_scenario("Scenario 3: Fused prediction with simulated weather", s3)
    run_scenario("Scenario 4: Fused prediction with aligned Open-Meteo weather", s4)
    run_scenario("Scenario 5: Low-confidence rejection / out-of-domain leaf", s5)
    run_scenario("Scenario 6: Knowledge base agricultural safety", s6)
    run_scenario("Scenario 7: SQLite persistence lifecycle", s7)
    run_scenario("Scenario 8: Local Crop Assistant AI chatbot", s8)
    run_scenario("Scenario 9: Multilingual UI & Accessibility integrity", s9)

    passed = sum(1 for _, st, _ in results if st == "PASS")
    print(f"\nTotal E2E Scenarios: {passed}/{len(results)} PASS")
