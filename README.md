# AI Crop Disease Prediction & Management (CropPulse AI)
**SIH Reference:** SIH1638 / Academic Assignment P05  
**Core Stack:** FastAPI, PyTorch MobileNetV2, Open-Meteo Historical Weather, SQLite, Vanilla HTML5/CSS3/ES6

CropPulse AI combines computer vision foliar diagnosis with an epidemiological environmental risk index based on plant pathology's Disease Triangle. It is designed for preventive decision-support and field review—never an uncalibrated diagnosis or a substitute for expert confirmation.

## Key Features & SIH Improvements

1. **Multimodal Late-Fusion Decision Support:**
   - Visual Classifier: MobileNetV2 (~3.5M parameters) trained on foliar disease patterns.
   - Microclimate Engine: Rule-based disease favorability assessing temperature, relative humidity, leaf wetness duration, and rainfall.
   - Decision Fusion: Transparent heuristic weighting ($W_{vision} = 0.65, W_{env} = 0.35$) with explicit contribution breakdown bars.
2. **Canonical Label Aliasing & Probability Aggregation:**
   - Consolidates 53 raw model classes (including duplicate folder naming variants for Tomato and Pepper) into **41 unique canonical biological classes** (38 official PlantVillage + 3 Rice classes).
   - Eliminates false low-confidence rejections caused by probability splitting across duplicate labels.
3. **Comprehensive Agronomic Knowledge Base (All 41 Canonical Classes):**
   - Pathogen-specific profiles distinguishing Fungal, Oomycete, Bacterial, Viral, Mite, and Healthy categories.
   - Safe integrated pest management (IPM): No synthetic fungicides prescribed for viral or bacterial diseases; healthy plants receive zero chemical controls.
   - Curated organic controls, approved chemicals with Pre-Harvest Intervals (PHI), and non-chemical cultural sanitation.
4. **Local SQLite Persistence & Telemetry (`crop_history.db`):**
   - Persistent diagnosis log recording timestamp, crop, canonical disease, confidence, risk score, weather mode, and SHA-256 image hashes.
   - REST endpoints at `/api/history` with a live visual telemetry list on the dashboard.
5. **Farmer Accessibility (Bilingual & Audio Guidance):**
   - Instant English / Hindi (`EN` | `हिन्दी`) localization toggle without page reload.
   - Browser-native speech synthesis (Web Speech API) to read treatment steps aloud to farmers with limited literacy.
6. **Robust Dual Safety Thresholding (Reject Option):**
   - Minimum confidence floor ($CONF_{MIN} = 50\%$) and top-1/top-2 margin check ($MARGIN_{MIN} = 15\%$).
   - HSV foliage ratio filter rejecting non-plant images ($<6\%$ plant tissue hue).
   - Maximum 25 MP resolution guard preventing image decompression bombs.

## Data Sources and Alignment

- **Images:** PlantVillage (`abdallahalidev/plantvillage-dataset` on Kaggle). Controlled lab specimens lacking farm coordinates or capture dates.
- **Weather:** Open-Meteo Historical Weather API. When capture latitude, longitude, and date are provided, daily weather parameters are retrieved. Leaf wetness is an explicitly labeled proxy estimate derived from relative humidity and precipitation.
- **Controlled Simulation:** If coordinates/date are omitted, user sliders or preset chips provide an unaligned simulation clearly labeled in the UI and API response.

The exact sources and limitations are also recorded in [dataset-metadata.json](./dataset-metadata.json).

## Quick Start

Use Python 3.10:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:8000> in your browser. Interactive API documentation is available at <http://127.0.0.1:8000/docs>.

### Run Automated Regression Tests

The project includes an automated test suite covering startup, image validation, probability aggregation, knowledge base coverage, chemical safety, persistence, and CORS security:

```powershell
python test_system.py
```

### Docker Container Build

```bash
docker build -t crop-pulse-ai .
docker run -p 8000:8000 crop-pulse-ai
```
*(Lean build context enabled via `.dockerignore`)*

## Core Architecture

- `backend/main.py` — FastAPI application entry point, CORS, and static file serving
- `backend/api/routes.py` — REST endpoints for image inference, weather, fusion, chatbot, and scan history
- `backend/database/db.py` — SQLite persistence layer (`crop_history.db`)
- `backend/database/knowledge_base.py` — 41-class disease profiles, triggers, and IPM treatments
- `backend/ml_engine/vision_classifier.py` — MobileNetV2 inference and canonical probability aggregation
- `backend/ml_engine/environmental_risk.py` — Rule-based microclimatic disease favorability
- `backend/ml_engine/weather_source.py` — Open-Meteo historical weather client
- `backend/ml_engine/fusion_engine.py` — Multimodal decision-support fusion engine
- `backend/ml_engine/crop_chatbot.py` — Local bilingual agronomist knowledge assistant
- `frontend/` — Single-page dashboard, bilingual UI, audio guidance, and history telemetry
- `test_system.py` — 24 automated unit/integration tests
