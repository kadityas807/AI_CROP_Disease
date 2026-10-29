"""
Main FastAPI Application Entry Point for SIH1638: AI-Driven Crop Disease Prediction and Management System
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.api.routes import router as api_router

# Initialize FastAPI App
app = FastAPI(
    title="AI-Driven Crop Disease Prediction & Management System",
    description="PlantVillage image classification with aligned public weather or controlled environmental risk inputs.",
    version="1.0.0"
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router)

# Mount Static Files for Web Dashboard Frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def serve_index():
    """Serve modern single-page dashboard UI."""
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "online", "message": "SIH1638 AI Backend Running. Frontend loading..."}

@app.get("/health")
async def health_check():
    """System health & readiness probe."""
    return {
        "status": "healthy",
        "system": "SIH1638 Crop Disease AI Platform",
        "engine": "PlantVillage vision model and rule-based environmental risk index"
    }
