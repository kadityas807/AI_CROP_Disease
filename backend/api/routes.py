"""Prediction API for PlantVillage image inference and environmental risk."""

import asyncio
from datetime import date
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.database.knowledge_base import get_disease_profile
from backend.database.db import crop_db
from backend.ml_engine.environmental_risk import env_risk_engine
from backend.ml_engine.fusion_engine import fusion_engine
from backend.ml_engine.crop_chatbot import crop_chatbot
from backend.ml_engine.vision_classifier import vision_classifier
from backend.ml_engine.weather_source import (
    WeatherSourceError,
    fetch_weather_for_observation,
)

router = APIRouter(prefix="/api")
MAX_IMAGE_BYTES = 10 * 1024 * 1024


class EnvironmentalInput(BaseModel):
    temperature: float = Field(..., ge=-10.0, le=55.0)
    relative_humidity: float = Field(..., ge=0.0, le=100.0)
    rainfall_mm: float = Field(0.0, ge=0.0, le=500.0)
    leaf_wetness_hours: float = Field(0.0, ge=0.0, le=24.0)
    wind_speed_kmh: float = Field(10.0, ge=0.0, le=150.0)
    crop_stage: str = "Vegetative"
    target_crop: str = "Tomato"
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    observation_date: Optional[date] = None


class ChatInput(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    predicted_class: Optional[str] = Field(None, max_length=120)
    environmental_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    fused_score: Optional[float] = Field(None, ge=0.0, le=100.0)


def _environmental_result(
    *,
    temperature: float,
    relative_humidity: float,
    rainfall_mm: float,
    leaf_wetness_hours: float,
    wind_speed_kmh: float,
    crop_stage: str,
    target_crop: str,
    latitude: Optional[float],
    longitude: Optional[float],
    observation_date: Optional[date],
) -> dict:
    supplied_alignment = (latitude is not None, longitude is not None, observation_date is not None)
    if any(supplied_alignment) and not all(supplied_alignment):
        raise HTTPException(
            status_code=422,
            detail="Provide latitude, longitude, and image observation date together, or omit all three for controlled simulation.",
        )

    if all(supplied_alignment):
        try:
            weather = fetch_weather_for_observation(
                latitude, longitude, observation_date
            )
        except WeatherSourceError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        weather_values = weather
        data_source = weather["source"]
    else:
        weather_values = {
            "temperature": temperature,
            "relative_humidity": relative_humidity,
            "rainfall_mm": rainfall_mm,
            "leaf_wetness_hours": leaf_wetness_hours,
            "wind_speed_kmh": wind_speed_kmh,
        }
        data_source = {
            "name": "User-entered controlled simulation",
            "spatially_aligned": False,
            "temporally_aligned": False,
            "notice": "These values are simulated inputs, not observed farm weather.",
        }

    result = env_risk_engine.compute_disease_vulnerability(
        temperature=weather_values["temperature"],
        relative_humidity=weather_values["relative_humidity"],
        rainfall_mm=weather_values["rainfall_mm"],
        leaf_wetness_hours=weather_values["leaf_wetness_hours"],
        wind_speed_kmh=weather_values["wind_speed_kmh"],
        crop_stage=crop_stage,
        target_crop=target_crop,
    )
    result["data_source"] = data_source
    result["score_interpretation"] = (
        "Rule-based environmental favorability index; not a calibrated disease probability."
    )
    return result


@router.get("/presets/weather")
async def get_weather_presets():
    """Return example inputs for explicitly controlled environmental simulations."""
    return env_risk_engine.presets


SAMPLE_LEAVES = [
    {
        "id": "tomato_early_blight",
        "title": "Tomato Early Blight",
        "crop": "Tomato",
        "badge": "🍅 Early Blight",
        "file_url": "/static/samples/tomato_early_blight.jpg",
        "filename": "tomato_early_blight.jpg",
        "is_low_conf": False,
        "description": "Alternaria solani concentric leaf spots with chlorotic halo",
    },
    {
        "id": "potato_late_blight",
        "title": "Potato Late Blight",
        "crop": "Potato",
        "badge": "🥔 Late Blight",
        "file_url": "/static/samples/potato_late_blight.jpg",
        "filename": "potato_late_blight.jpg",
        "is_low_conf": False,
        "description": "Phytophthora infestans water-soaked lesions under high humidity",
    },
    {
        "id": "tomato_healthy",
        "title": "Tomato Healthy",
        "crop": "Tomato",
        "badge": "🌿 Healthy Tomato",
        "file_url": "/static/samples/tomato_healthy.jpg",
        "filename": "tomato_healthy.jpg",
        "is_low_conf": False,
        "description": "Vibrant foliage with zero active lesions",
    },
    {
        "id": "corn_common_rust",
        "title": "Corn Common Rust",
        "crop": "Corn (Maize)",
        "badge": "🌽 Common Rust",
        "file_url": "/static/samples/corn_common_rust.jpg",
        "filename": "corn_common_rust.jpg",
        "is_low_conf": False,
        "description": "Puccinia sorghi cinnamon-brown pustules on corn leaf",
    },
    {
        "id": "ambiguous_sample",
        "title": "Ambiguous Noise",
        "crop": "Tomato",
        "badge": "⚠️ Ambiguous (Low Conf Test)",
        "file_url": "/static/samples/ambiguous_sample.jpg",
        "filename": "ambiguous_sample.jpg",
        "is_low_conf": True,
        "description": "Demonstrates P05-A low-confidence rejection & safety alert",
    },
]


@router.get("/samples/leaves")
async def get_sample_leaves():
    """Return curated sample leaf images for interactive demonstration and testing."""
    return SAMPLE_LEAVES


@router.post("/chat")
async def chat_with_crop_assistant(payload: ChatInput):
    """Answer crop-help questions using local project knowledge, without external AI services."""
    return await asyncio.to_thread(crop_chatbot.answer, **payload.model_dump())


@router.post("/predict/environmental")
async def predict_environmental_risk(payload: EnvironmentalInput):
    return _environmental_result(**payload.model_dump())


@router.post("/predict/image")
async def predict_crop_image(
    file: UploadFile = File(...),
    crop_hint: Optional[str] = Form(None),
):
    contents = await file.read(MAX_IMAGE_BYTES + 1)
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(contents) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image exceeds the 10 MiB upload limit.")
    try:
        vision_result = await asyncio.to_thread(vision_classifier.predict, contents, crop_hint=crop_hint)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "status": "success",
        "vision_diagnosis": vision_result,
        "disease_profile": get_disease_profile(vision_result["predicted_class"]),
    }



@router.get("/history")
async def get_diagnosis_history(limit: int = 20):
    """Return recent scan history records."""
    return crop_db.get_recent_scans(limit=min(limit, 50))


@router.delete("/history")
async def clear_diagnosis_history():
    """Clear saved scan history."""
    count = crop_db.clear_history()
    return {"status": "success", "deleted_count": count}

@router.post("/predict/fused")
async def predict_multimodal_fused(
    file: UploadFile = File(...),
    temperature: float = Form(23.5, ge=-10.0, le=55.0),
    relative_humidity: float = Form(88.0, ge=0.0, le=100.0),
    rainfall_mm: float = Form(15.0, ge=0.0, le=500.0),
    leaf_wetness_hours: float = Form(8.0, ge=0.0, le=24.0),
    wind_speed_kmh: float = Form(12.0, ge=0.0, le=150.0),
    crop_stage: str = Form("Vegetative"),
    target_crop: str = Form("Tomato"),
    latitude: Optional[float] = Form(None, ge=-90.0, le=90.0),
    longitude: Optional[float] = Form(None, ge=-180.0, le=180.0),
    observation_date: Optional[date] = Form(None),
):
    image_bytes = await file.read(MAX_IMAGE_BYTES + 1)
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image exceeds the 10 MiB upload limit.")

    try:
        vision_result = await asyncio.to_thread(vision_classifier.predict, image_bytes, crop_hint=target_crop)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    environmental_result = _environmental_result(
        temperature=temperature,
        relative_humidity=relative_humidity,
        rainfall_mm=rainfall_mm,
        leaf_wetness_hours=leaf_wetness_hours,
        wind_speed_kmh=wind_speed_kmh,
        crop_stage=crop_stage,
        target_crop=target_crop,
        latitude=latitude,
        longitude=longitude,
        observation_date=observation_date,
    )
    fusion_result = fusion_engine.fuse(
        vision_result=vision_result,
        environmental_result=environmental_result,
        crop_hint=target_crop,
    )

    # P05-C: Label weather source explicitly in the response
    is_aligned = all([latitude, longitude, observation_date])
    weather_source_label = "open-meteo" if is_aligned else "simulated"

    env_details = dict(environmental_result)
    env_details["weather_source"] = weather_source_label
    if not is_aligned:
        env_details.setdefault("data_source", {})["spatially_aligned"] = False

    # Persist scan to local SQLite history
    scan_id = None
    try:
        scan_id = crop_db.save_scan(
            crop=target_crop,
            predicted_class=vision_result["predicted_class"],
            disease_name=fusion_result.get("disease_name", vision_result["display_name"]),
            confidence=vision_result["confidence"],
            confidence_status=vision_result.get("confidence_status", "ok"),
            risk_score=fusion_result["fused_risk_score"],
            weather_source=weather_source_label,
            temperature=env_details["parameters"]["temperature"],
            humidity=env_details["parameters"]["relative_humidity"],
            rainfall=env_details["parameters"]["rainfall_mm"],
            image_bytes=image_bytes,
        )
    except Exception:
        scan_id = None

    return {
        "status": "success",
        "scan_id": scan_id,
        "multimodal_fusion": fusion_result,
        "vision_details": vision_result,
        "environmental_details": env_details,
    }
