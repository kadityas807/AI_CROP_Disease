# Project guide

## Purpose

AI Crop Disease Prediction & Management combines two required signals:

1. A MobileNetV2 image classifier predicts a disease class from a crop-leaf image.
2. A transparent environmental risk index evaluates temperature, humidity, rainfall, leaf wetness, and crop stage.

The fused output is a decision-support risk index with existing disease-specific preventive guidance. Neither the fused index nor the environmental index is a calibrated probability.

## Data flow

1. The user uploads an image and chooses its crop.
2. If the capture location and date are known, the backend retrieves historical daily weather for that coordinate/date from Open-Meteo and records the source and alignment metadata in the response.
3. Otherwise, user-entered values or presets are clearly labeled controlled simulation inputs.
4. The image model and environmental rules run independently; the fusion code combines their outputs and returns guidance for field review.

PlantVillage images do not carry reliable farm coordinates or capture dates. The app therefore does not invent an image-to-weather match. Read [README.md](./README.md) for dataset citations, run instructions, and known model limitations.

## Main files

- `backend/ml_engine/vision_classifier.py`: preprocessing, checkpoint loading, and image inference
- `backend/ml_engine/weather_source.py`: public historical weather retrieval and alignment metadata
- `backend/ml_engine/environmental_risk.py`: environmental score and controlled simulation presets
- `backend/ml_engine/fusion_engine.py`: fused risk index and preventive guidance
- `backend/api/routes.py`: API endpoints for image, environmental, and fused predictions
- `frontend/index.html` and `frontend/js/app.js`: upload, environmental inputs, and prediction display
- `training/01_dataset_setup.py` and `training/02_train_vision_model.py`: PlantVillage-only split and model training
- `test_system.py`: inference, risk-index, and metadata-alignment tests

## Important limitations

- The existing checkpoint has a 53-class mapping and its original training provenance is not documented. The corrected training pipeline targets the 38 official PlantVillage color classes; retrain before claiming the checked-in checkpoint was trained only on PlantVillage.
- The environmental score is based on transparent rules, not independently labeled disease outcomes. No accuracy or epidemiological validation claim is made.
- Open-Meteo provides daily weather, not measured leaf wetness. The returned leaf-wetness value is explicitly labeled as an estimate from humidity and precipitation.
