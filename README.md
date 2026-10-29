# AI Crop Disease Prediction & Management

This project predicts a crop-leaf class from an uploaded image and combines the image-model output with an environmental disease-favorability index. It supports preventive field review; it is not a calibrated diagnosis or a substitute for expert confirmation.

## Data sources and alignment

- **Images:** PlantVillage, `abdallahalidev/plantvillage-dataset` on Kaggle: <https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset>. The controlled PlantVillage images do not provide farm coordinates or capture dates.
- **Weather:** Open-Meteo Historical Weather API: <https://open-meteo.com/en/docs/historical-weather-api>. When the image's latitude, longitude, and capture date are provided together, the API retrieves that location's daily mean temperature, relative humidity, precipitation, and maximum wind speed for that date. Leaf wetness is an explicitly labeled estimate derived from humidity and precipitation; it is not an observed dataset field.
- **Simulation:** If image metadata is unavailable, leave all three location/date fields blank and use the labeled manual inputs or a preset. Such a run is an unaligned controlled simulation, not a real weather linkage.

The exact sources and limitations are also recorded in [dataset-metadata.json](./dataset-metadata.json).

## Run

Use Python 3.10, which matches the pinned PyTorch runtime and the Docker image.

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:8000>. Upload a leaf image, select its crop, and optionally enter the image capture coordinates and date. The app reports the source and alignment status with the environmental score.

The **Ask the crop assistant** section answers questions about the latest prediction, reference symptoms, preventive guidance, environmental scores, and the project workflow. It runs locally from the project's disease knowledge base and prediction context; it does not call a hosted generative AI model and needs no API key. Its answers are bounded by the saved knowledge and are not a substitute for expert advice.

For a clean PlantVillage-only training split (38 classes):

```powershell
python training/01_dataset_setup.py
python training/02_train_vision_model.py
```

The setup script uses the local PlantVillage color data when available; otherwise it needs Kaggle CLI credentials to download the dataset. Training uses a train/validation split and saves the weights and class mapping in `models/`.

To evaluate the existing checkpoint without training it again, run:

```powershell
python training/03_evaluate_vision_model.py
```

This evaluates the saved checkpoint against `data/processed/PlantVillage_Split/val`, which must have exactly the same class folders as `models/vision_classes.txt`. It writes per-class precision, recall, and F1 plus aggregate metrics to `reports/vision_validation_metrics.json`. The saved checkpoint currently has 53 labels, so this command uses its matching 53-class validation split; it will deliberately reject the separate 38-class official split. These are validation results, not an independent final test estimate, because validation data may have informed model selection.

Run the project tests with:

```powershell
python test_system.py
```

## Model and limitations

- Vision inference uses the trained MobileNetV2 checkpoint and its saved class mapping, with resize, center crop, and ImageNet normalization. Missing or invalid model artifacts stop startup; inference errors do not fall back to invented predictions.
- Environmental risk is a transparent rule-based index using temperature, humidity, rain, leaf-wetness proxy, and crop-stage adjustment. It is **not** trained on independently observed disease outcomes, and no accuracy claim is made.
- The existing checkpoint maps 53 labels and matches the legacy 53-class validation split. The clean PlantVillage setup pipeline creates 38 classes, so that checkpoint is not interchangeable with the 38-class split. Use the evaluator to check the existing model without retraining; do not claim it is a 38-class model or report validation metrics as an independent test result.
- PlantVillage lacks image-level spatial/temporal metadata. Real weather alignment is possible only when the user supplies trustworthy capture coordinates/date; otherwise the app labels the run as simulation.

## Core structure

- `backend/ml_engine/vision_classifier.py` — MobileNetV2 image inference
- `backend/ml_engine/environmental_risk.py` — environmental favorability rules and simulation presets
- `backend/ml_engine/weather_source.py` — Open-Meteo historical weather lookup
- `backend/ml_engine/fusion_engine.py` — combined risk index and disease-specific preventive guidance
- `backend/ml_engine/crop_chatbot.py` — local knowledge-base-backed crop question assistant
- `backend/api/routes.py` — prediction API
- `frontend/` — image upload, environmental inputs, and result display
- `training/` — PlantVillage download/split and image-model training
