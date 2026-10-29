"""Combine leaf-model output and environmental favorability into a risk index."""

from typing import Dict, Any
from backend.database.knowledge_base import get_disease_profile

# P05-B: Heuristic fusion weights -- documented, not calibrated.
W_VISION = 0.65
W_ENV = 0.35


class MultimodalFusionEngine:
    def fuse(
        self,
        vision_result: Dict[str, Any],
        environmental_result: Dict[str, Any],
        crop_hint: str = None
    ) -> Dict[str, Any]:
        """
        Synthesize visual detection and climatic predispositions into an actionable decision matrix.
        Weights: W_VISION=0.65 (photo evidence) / W_ENV=0.35 (field conditions).
        These are heuristic weights and are NOT calibrated probabilities.
        """
        predicted_class = vision_result["predicted_class"]
        visual_conf = vision_result["confidence"]
        is_healthy = vision_result["is_healthy"]

        disease_profile = get_disease_profile(predicted_class)
        env_score = environmental_result["composite_risk_score"]

        # Determine Pathogen-Specific Environmental Alignment
        triggers = disease_profile.get("bioclimatic_triggers", {})
        temp = environmental_result["parameters"]["temperature"]
        hum = environmental_result["parameters"]["relative_humidity"]
        data_source = environmental_result.get("data_source", {})
        is_simulated = not (
            data_source.get("spatially_aligned", False)
            and data_source.get("temporally_aligned", False)
        )

        temp_min = triggers.get("temp_min", 10.0)
        temp_max = triggers.get("temp_max", 35.0)
        hum_thresh = triggers.get("humidity_threshold", 75.0)

        is_temp_optimal = (temp_min <= temp <= temp_max)
        is_humidity_high = (hum >= hum_thresh)

        alignment_score = 0.0
        if is_temp_optimal:
            alignment_score += 0.5
        if is_humidity_high:
            alignment_score += 0.5

        # P05-B: Transparent fused risk with contribution tracking
        if is_healthy:
            # For healthy plants: risk is driven entirely by environmental pressure
            fused_risk_score = round(float(env_score * W_ENV), 1)
            urgency = "Normal / Preventative Monitoring" if env_score < 60 else "Elevated Environmental Threat"
            action_code = "MONITOR"
            vision_contribution = 0
            environment_contribution = round(fused_risk_score)
        else:
            # Disease detected visually: fuse vision + environment
            v_raw = W_VISION * visual_conf * 100
            e_raw = W_ENV * env_score
            fused_risk_score = round(float(v_raw + e_raw), 1)
            fused_risk_score = min(99.9, max(10.0, fused_risk_score))
            vision_contribution = round(v_raw)
            environment_contribution = round(e_raw)

            if fused_risk_score >= 80:
                urgency = "Very high index -- prompt field confirmation recommended"
                action_code = "FIELD_CONFIRMATION"
            elif fused_risk_score >= 60:
                urgency = "High index -- preventive field review recommended"
                action_code = "PREVENTIVE_REVIEW"
            elif fused_risk_score >= 40:
                urgency = "Moderate Infection -- Targeted Bio-Control"
                action_code = "ORGANIC_CONTROL"
            else:
                urgency = "Low Infection Severity -- Cultural Management"
                action_code = "CULTURAL_MANAGEMENT"

        common_name = disease_profile.get("common_name", predicted_class)
        reasoning_summary = []
        if visual_conf > 0.5:
            reasoning_summary.append(
                f"Leaf image pattern strongly matches the disease profile for {common_name}."
            )
        else:
            reasoning_summary.append(
                "Leaf image pattern is only moderately clear; field confirmation is advised."
            )
        if is_humidity_high and is_simulated:
            reasoning_summary.append(
                "The simulated humidity and wetness inputs may favor pathogen spread; they are not observed farm conditions."
            )
        elif is_humidity_high:
            reasoning_summary.append(
                "Observed humidity and wetness conditions may favor pathogen spread and disease development."
            )
        elif is_simulated:
            reasoning_summary.append(
                "The simulated environmental inputs do not strongly favor disease spread; they are not observed farm conditions."
            )
        else:
            reasoning_summary.append(
                "Observed environmental conditions are not strongly favoring disease spread."
            )
        if is_simulated and alignment_score >= 0.8:
            reasoning_summary.append(
                "The simulated inputs match some weather patterns associated with this disease, but this does not increase confidence in the image match."
            )
        elif is_simulated:
            reasoning_summary.append(
                "The simulated inputs are only a weather-pattern comparison and do not establish field conditions or validate the image match."
            )
        elif alignment_score >= 0.8:
            reasoning_summary.append(
                "Observed weather fits this disease profile; this is context, not confirmation of the image match."
            )
        else:
            reasoning_summary.append(
                "Observed weather and disease profile are only partially aligned; field confirmation remains important."
            )

        if is_simulated:
            weather_match = (
                "High Match (simulated inputs only)"
                if alignment_score >= 0.8
                else "Moderate Match (simulated inputs only)"
            )
        else:
            weather_match = (
                "High Match (Favorable for Spore Proliferation)"
                if alignment_score >= 0.8
                else "Moderate Match"
            )

        management = disease_profile.get("management", {})
        return {
            "fused_risk_score": fused_risk_score,
            "urgency_level": urgency,
            "action_code": action_code,
            "disease_name": common_name,
            "pathogen_type": disease_profile.get("pathogen_type", "Pathogen"),
            "causal_agent": disease_profile.get("causal_agent", "Microbe"),
            "crop": disease_profile.get("crop", "Crop"),
            "is_healthy": is_healthy,
            "visual_confidence_pct": vision_result["percentage"],
            "environmental_risk_score": env_score,
            "pathogen_weather_match": weather_match,
            # P05-B: Contribution bars -- show how the risk index is built
            "vision_contribution": vision_contribution,
            "environment_contribution": environment_contribution,
            "fusion_weights": {
                "W_VISION": W_VISION,
                "W_ENV": W_ENV,
                "note": "Heuristic weights, not calibrated probabilities.",
            },
            "reasoning_summary": reasoning_summary,
            "symptoms_identified": disease_profile.get("symptoms", []),
            "treatment_plan": {
                "immediate_interventions": management.get("preventive_intervention", []),
                "organic_remedies": management.get("organic_controls", []),
                "chemical_controls": management.get("chemical_controls", []),
                "cultural_guidance": management.get("cultural_practices", "")
            }
        }


# Global singleton
fusion_engine = MultimodalFusionEngine()
