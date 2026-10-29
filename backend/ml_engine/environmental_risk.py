"""Transparent rule-based environmental disease-favorability scoring."""

from typing import Dict, Any
import numpy as np

class EnvironmentalRiskEngine:
    def __init__(self):
        # Presets are explicitly controlled simulations, not weather observations.
        self.presets = {
            "monsoon_high_humidity": {
                "name": "Monsoon / Rainy Outbreak (High Risk)",
                "temperature": 23.5,
                "relative_humidity": 92.0,
                "rainfall_mm": 35.0,
                "leaf_wetness_hours": 12.0,
                "wind_speed_kmh": 14.0,
                "description": "Prolonged leaf wetness and warm-temperate humidity favor rapid oomycete and fungal sporulation."
            },
            "cloudy_cool_fog": {
                "name": "Cool, humid, and wet",
                "temperature": 16.5,
                "relative_humidity": 95.0,
                "rainfall_mm": 5.0,
                "leaf_wetness_hours": 14.0,
                "wind_speed_kmh": 6.0,
                "description": "A controlled example of cool temperatures, high humidity, and prolonged leaf wetness."
            },
            "warm_humid_tropical": {
                "name": "Warm & Humid Tropical (Bacterial & Early Blight)",
                "temperature": 29.0,
                "relative_humidity": 82.0,
                "rainfall_mm": 15.0,
                "leaf_wetness_hours": 7.0,
                "wind_speed_kmh": 18.0,
                "description": "Favors Xanthomonas bacterial spot and Alternaria conidial germination."
            },
            "dry_hot_summer": {
                "name": "Dry Hot Summer (Low Disease Risk / Vector Pest Window)",
                "temperature": 36.0,
                "relative_humidity": 38.0,
                "rainfall_mm": 0.0,
                "leaf_wetness_hours": 1.0,
                "wind_speed_kmh": 22.0,
                "description": "Low fungal vulnerability; watch for spider mites and drought stress."
            },
            "optimal_healthy_greenhouse": {
                "name": "Controlled Greenhouse / Optimal Weather",
                "temperature": 22.0,
                "relative_humidity": 55.0,
                "rainfall_mm": 0.0,
                "leaf_wetness_hours": 1.5,
                "wind_speed_kmh": 8.0,
                "description": "Balanced environmental parameters minimize pathogen survival."
            }
        }

    def compute_disease_vulnerability(
        self,
        temperature: float,
        relative_humidity: float,
        rainfall_mm: float,
        leaf_wetness_hours: float,
        wind_speed_kmh: float = 10.0,
        crop_stage: str = "Vegetative",
        target_crop: str = "Tomato"
    ) -> Dict[str, Any]:
        """
        Calculate quantitative biological infection indices based on micro-climatic criteria.
        """
        # 1. Fungal Pathogen Index (Requires wet leaf surface + moderate temps)
        # Thermal suitability bell-curve peaking around 20-25°C
        temp_fungal_factor = max(0.0, 1.0 - ((temperature - 22.5) / 13.0) ** 2)
        humidity_fungal_factor = max(0.0, (relative_humidity - 50.0) / 50.0)
        wetness_factor = min(1.0, leaf_wetness_hours / 10.0)
        rain_factor = min(1.0, rainfall_mm / 25.0)
        
        fungal_risk_raw = (
            temp_fungal_factor * 0.30 +
            humidity_fungal_factor * 0.35 +
            wetness_factor * 0.25 +
            rain_factor * 0.10
        )
        fungal_risk_pct = round(float(np.clip(fungal_risk_raw * 100.0, 0, 100)), 1)

        # 2. Oomycete / Late Blight Index (Favors cooler temps 14-21°C + high humidity > 85% + prolonged leaf wetness)
        temp_blight_factor = max(0.0, 1.0 - ((temperature - 17.5) / 8.0) ** 2)
        hum_blight_factor = 1.0 if relative_humidity >= 88 else max(0.0, (relative_humidity - 65) / 25)
        late_blight_risk_raw = (temp_blight_factor * 0.35 + hum_blight_factor * 0.40 + wetness_factor * 0.25)
        late_blight_risk_pct = round(float(np.clip(late_blight_risk_raw * 100.0, 0, 100)), 1)

        # 3. Bacterial Infection Index (Favors warmer temps 25-34°C + splashing rain/wind)
        temp_bacterial_factor = max(0.0, 1.0 - ((temperature - 29.0) / 10.0) ** 2)
        wind_rain_splash = min(1.0, (wind_speed_kmh / 20.0) * (rainfall_mm / 15.0 + 0.2))
        bacterial_risk_raw = (
            temp_bacterial_factor * 0.35 +
            humidity_fungal_factor * 0.35 +
            wind_rain_splash * 0.30
        )
        bacterial_risk_pct = round(float(np.clip(bacterial_risk_raw * 100.0, 0, 100)), 1)

        # 4. Crop Growth Stage Vulnerability Multiplier
        stage_multipliers = {
            "Seedling": 1.15,
            "Vegetative": 1.0,
            "Flowering": 1.25,  # High vulnerability
            "Fruiting": 1.20,
            "Maturity / Harvest": 0.90
        }
        stage_mult = stage_multipliers.get(crop_stage, 1.0)

        # Overall composite environmental risk score (Heuristic Default)
        composite_risk = (fungal_risk_pct * 0.45 + late_blight_risk_pct * 0.35 + bacterial_risk_pct * 0.20) * stage_mult
        composite_risk = round(float(np.clip(composite_risk, 0, 100)), 1)

        # This is a transparent heuristic index, not a calibrated probability.
        if composite_risk >= 75:
            severity = "Very high environmental favorability"
            badge_color = "#ef4444"
        elif composite_risk >= 50:
            severity = "High environmental favorability"
            badge_color = "#f97316"
        elif composite_risk >= 30:
            severity = "Moderate environmental favorability"
            badge_color = "#eab308"
        else:
            severity = "Low environmental favorability"
            badge_color = "#22c55e"

        # Trigger explanations
        triggers = []
        if relative_humidity >= 85:
            triggers.append(f"Relative humidity ({relative_humidity}%) is above critical spore germination threshold (85%)")
        if leaf_wetness_hours >= 7:
            triggers.append(f"Leaf wetness duration ({leaf_wetness_hours} hrs) exceeds infection initiation period")
        if 14.0 <= temperature <= 22.0 and relative_humidity >= 80:
            triggers.append(f"Temperature ({temperature}°C) sits directly in the Late Blight / Oomycete optimal infection band")
        elif 25.0 <= temperature <= 32.0 and rainfall_mm > 5:
            triggers.append(f"Warm rainfall provides ideal conditions for Xanthomonas bacterial multiplication")
        if not triggers:
            triggers.append("Environmental variables are within safe agronomic parameters")

        return {
            "composite_risk_score": composite_risk,
            "severity_level": severity,
            "badge_color": badge_color,
            "sub_indices": {
                "fungal_risk": fungal_risk_pct,
                "late_blight_risk": late_blight_risk_pct,
                "bacterial_risk": bacterial_risk_pct
            },
            "parameters": {
                "temperature": temperature,
                "relative_humidity": relative_humidity,
                "rainfall_mm": rainfall_mm,
                "leaf_wetness_hours": leaf_wetness_hours,
                "wind_speed_kmh": wind_speed_kmh,
                "crop_stage": crop_stage,
                "target_crop": target_crop
            },
            "active_triggers": triggers
        }

# Global singleton
env_risk_engine = EnvironmentalRiskEngine()
