"""
Launcher script for AI Crop Disease Prediction and Management System
Starts FastAPI server with Uvicorn on http://127.0.0.1:8000
"""

import uvicorn
import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("AI Crop Disease Prediction & Management")
    print("Server starting at: http://127.0.0.1:8000")
    print("Interactive API docs: http://127.0.0.1:8000/docs")
    print("="*70 + "\n")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
