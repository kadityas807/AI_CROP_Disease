"""
SQLite persistence layer for AI Crop Disease Prediction history.
Provides lightweight, reliable storage for diagnosis scans and field telemetry.
"""

import hashlib
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class CropDatabase:
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            env_path = os.getenv("CROP_DB_PATH")
            if env_path:
                db_path = Path(env_path)
            else:
                project_root = Path(__file__).resolve().parents[2]
                db_path = project_root / "crop_history.db"
        self.db_path = str(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=15.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        conn = self._get_connection()
        try:
            with conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS diagnosis_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        crop TEXT NOT NULL,
                        predicted_class TEXT NOT NULL,
                        disease_name TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        confidence_status TEXT NOT NULL,
                        risk_score REAL NOT NULL,
                        weather_source TEXT NOT NULL,
                        temperature REAL,
                        humidity REAL,
                        rainfall REAL,
                        image_hash TEXT
                    )
                """)
                conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON diagnosis_history(timestamp DESC)")
        finally:
            conn.close()

    @staticmethod
    def compute_image_hash(image_bytes: bytes) -> str:
        return hashlib.sha256(image_bytes).hexdigest()[:16]

    def save_scan(
        self,
        crop: str,
        predicted_class: str,
        disease_name: str,
        confidence: float,
        confidence_status: str,
        risk_score: float,
        weather_source: str,
        temperature: Optional[float] = None,
        humidity: Optional[float] = None,
        rainfall: Optional[float] = None,
        image_bytes: Optional[bytes] = None,
    ) -> int:
        img_hash = self.compute_image_hash(image_bytes) if image_bytes else None
        now_utc = datetime.now(timezone.utc).isoformat()
        conn = self._get_connection()
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO diagnosis_history (
                        timestamp, crop, predicted_class, disease_name,
                        confidence, confidence_status, risk_score,
                        weather_source, temperature, humidity, rainfall, image_hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        now_utc,
                        crop,
                        predicted_class,
                        disease_name,
                        round(float(confidence), 4),
                        confidence_status,
                        round(float(risk_score), 1),
                        weather_source,
                        round(float(temperature), 1) if temperature is not None else None,
                        round(float(humidity), 1) if humidity is not None else None,
                        round(float(rainfall), 1) if rainfall is not None else None,
                        img_hash,
                    ),
                )
                return int(cursor.lastrowid)
        finally:
            conn.close()

    def get_recent_scans(self, limit: int = 20) -> List[Dict[str, Any]]:
        safe_limit = max(1, min(int(limit), 100))
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                """
                SELECT id, timestamp, crop, predicted_class, disease_name,
                       confidence, confidence_status, risk_score, weather_source,
                       temperature, humidity, rainfall, image_hash
                FROM diagnosis_history
                ORDER BY id DESC
                LIMIT ?
                """,
                (safe_limit,),
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def clear_history(self) -> int:
        conn = self._get_connection()
        try:
            with conn:
                cursor = conn.execute("DELETE FROM diagnosis_history")
                return cursor.rowcount
        finally:
            conn.close()


# Global singleton instance
crop_db = CropDatabase()
