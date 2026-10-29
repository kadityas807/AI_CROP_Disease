"""
Main FastAPI Application Entry Point for SIH1638: AI-Driven Crop Disease Prediction and Management System
"""

import os
import time
from fastapi import FastAPI, Request
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

# High-Performance Concurrency Profiling Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000.0
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response

# CORS Middleware Setup (Secure configuration per SIH specifications)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
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
    """System health & readiness probe with architecture diagnostics."""
    return {
        "status": "healthy",
        "system": "SIH1638 Crop Disease AI Platform",
        "engine": "PlantVillage vision model and rule-based environmental risk index",
        "concurrency_mode": "asynchronous non-blocking worker threadpool",
        "version": "1.0.0"
    }
