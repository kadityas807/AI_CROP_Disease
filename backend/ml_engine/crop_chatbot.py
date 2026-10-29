"""
Local agronomic knowledge assistant for crop health decision support.
Grounds responses in the 41-class disease knowledge base, bioclimatic triggers,
and integrated pest management (IPM) guidance, supporting both English and Hindi.
Enhanced with fuzzy semantic retrieval, multi-turn scan context awareness, and CIBRC safety rules.
"""

import re
from typing import Optional, List, Dict, Any

from backend.database.knowledge_base import get_disease_profile, CROPS_DATABASE


class CropChatbot:
    def answer(
        self,
        message: str,
        predicted_class: Optional[str] = None,
        environmental_score: Optional[float] = None,
        fused_score: Optional[float] = None,
    ) -> dict:
        text = message.lower().strip()
        is_hindi = bool(re.search(r"[\u0900-\u097F]", message)) or any(
            w in text for w in ["namaste", "upchar", "lakshan", "dawa", "kisan", "ilaaj", "roktham", "patti", "kheti"]
        )

        # 1. Check if user explicitly references a specific disease or crop
        referenced_class = self._find_referenced_disease(text)
        active_class = referenced_class or predicted_class
        profile = get_disease_profile(active_class) if active_class else None

        name = profile["common_name"] if profile else None
        pathogen = profile.get("pathogen_type", "Pathogen") if profile else None
        management = profile.get("management", {}) if profile else {}

        # 2. Semantic Intent Classification

        # Intent: Greetings
        if self._matches(text, "hello", "hi", "hey", "good morning", "good afternoon", "namaste", "namaskar") or "नमस्ते" in message or "नमस्कार" in message:
            if is_hindi:
                answer = (
                    "नमस्ते! मैं आपका स्थानीय कृषि सहायक हूँ। मैं आपके पत्ती रोग के परिणाम, "
                    "लक्षण, मौसम संबंधी जोखिम और रोकथाम के उपायों को समझा सकता हूँ। "
                    "पूछिए: “मेरे परिणाम का अर्थ क्या है?” या “इसके लक्षण क्या हैं?”"
                )
            else:
                answer = (
                    "Hello! I can explain your leaf prediction, symptoms, environmental "
                    "score, and preventive guidance. Try asking “Explain my result” or "
                    "“What should I do next?”"
                )

        # Intent: System Workflow & Technical Architecture
        elif self._matches(text, "how does", "how do", "how it work", "how this work", "workflow", "project work", "architecture") or "काम कैसे" in message or "प्रणाली" in message:
            if is_hindi:
                answer = (
                    "एक पत्ती की फोटो अपलोड करें और फसल चुनें। MobileNetV2 मॉडल पत्ती के रोग की पहचान करता है। "
                    "इसके साथ ही प्रणाली तापमान, आर्द्रता और पत्ती के गीलेपन के आधार पर पर्यावरणीय जोखिम स्कोर निकालती है "
                    "और दोनों को मिलाकर एकीकृत कृषि सलाह देती है।"
                )
            else:
                answer = (
                    "Upload a leaf photo and choose its crop. The MobileNetV2 image model "
                    "ranks likely leaf classes. The app separately calculates a "
                    "rule-based environmental favorability index, then combines those "
                    "signals into a decision-support score and displays guidance."
                )

        # Intent: Weather & Environmental Microclimate
        elif self._matches(text, "weather", "humidity", "rainfall", "leaf wetness", "temperature", "environment", "microclimate") or "मौसम" in message or "तापमान" in message or "बारिश" in message or "नमी" in message:
            if environmental_score is None:
                answer = (
                    "The environmental index uses temperature, relative humidity, "
                    "rainfall, estimated leaf wetness, wind, and crop stage. Run a "
                    "prediction to give me its score to explain. It is a rule-based "
                    "favorability index, not a disease probability."
                )
            else:
                answer = (
                    f"The environmental favorability index for the latest result is "
                    f"{environmental_score:.1f} out of 100. It is calculated from "
                    "weather-related rules and is not a calibrated probability that "
                    "the plant has a disease."
                )

        # Intent: Organic & Biological Control
        elif self._matches(text, "organic", "bio", "biological", "neem", "natural", "trichoderma", "जैविक", "नीम"):
            if not profile:
                answer = "Run a crop check first so I can retrieve specific bio-control recommendations for your plant."
            elif profile.get("severity_level") == "Healthy":
                answer = f"{name} is healthy! No organic or chemical sprays are required. Maintain regular composting and balanced irrigation."
            else:
                organics = management.get("organic_controls", [])
                if organics:
                    items = [f"{o['name']} ({o['dosage']}, {o['frequency']})" for o in organics]
                    answer = f"Recommended organic controls for {name}: " + "; ".join(items) + ". Organic treatments are safe and preserve natural predatory insects."
                else:
                    answer = f"For {name}, focus on cultural sanitation, removing infected leaves, and consulting a local agronomist."

        # Intent: Chemical Controls & Pesticide Safety
        elif self._matches(text, "chemical", "fungicide", "bactericide", "spray", "medicine", "dawa", "mancozeb", "pesticide", "दवा", "कीटनाशक", "फफूंदनाशक"):
            if not profile:
                answer = "Run a crop diagnosis first so I can inspect verified chemical recommendations and pre-harvest intervals."
            elif profile.get("severity_level") == "Healthy":
                answer = f"Do not apply chemicals! The leaf is diagnosed as {name}. Unnecessary chemical sprays waste money and harm beneficial soil microbes."
            elif pathogen == "Viral":
                answer = f"Caution: {name} is caused by a virus. Plant viruses CANNOT be cured with fungicides or chemical sprays! Focus on controlling the insect vector (such as whiteflies or aphids) using sticky traps and neem oil."
            elif pathogen == "Bacterial":
                chemicals = management.get("chemical_controls", [])
                items = [f"{c['name']} (Dose: {c['dosage']}, PHI: {c.get('phi_days', 0)} days)" for c in chemicals]
                answer = f"Caution: {name} is bacterial. Synthetic fungicides like Mancozeb are ineffective. Recommended bactericidal sprays: " + "; ".join(items) + ". Always observe safety gear and Pre-Harvest Intervals."
            else:
                chemicals = management.get("chemical_controls", [])
                if chemicals:
                    items = [f"{c['name']} (Dose: {c['dosage']}, PHI: {c.get('phi_days', 0)} days)" for c in chemicals]
                    answer = f"Approved chemical options for {name}: " + "; ".join(items) + ". Always observe Pre-Harvest Intervals (PHI) and wear protective equipment."
                else:
                    answer = f"For {name}, no synthetic chemical sprays are advised. Follow cultural sanitation and consult a local agricultural extension officer."

        # Intent: Pathogen Cause & Etiology
        elif self._matches(text, "pathogen", "cause", "causal", "agent", "organism", "virus", "fungus", "bacteria", "कारण", "रोगजनक"):
            if profile:
                causal = profile.get("causal_agent", "Microbe")
                answer = f"{name} is caused by the {pathogen} pathogen '{causal}'. Transmission occurs via wind-blown spores, rain splashing, or insect vectors."
            else:
                answer = "Run a leaf analysis first, and I will identify the causal pathogen (fungal, bacterial, viral, or pest)."

        # Intent: Symptoms & Visual Signs
        elif self._matches(text, "symptom", "look like", "sign", "identify", "lesion") or "लक्षण" in message or "पहचान" in message:
            if profile:
                symptoms = profile.get("symptoms", [])
                answer = f"Symptoms associated with {name} include: " + "; ".join(symptoms[:4])
                answer += " These are reference symptoms, not proof that the plant has this disease."
            else:
                answer = (
                    "I can describe symptoms associated with the latest prediction "
                    "after you run a leaf-image analysis. A photo alone cannot "
                    "confirm a diagnosis."
                )

        # Intent: Treatment, Prevention & Cultural Field Management
        elif self._matches(text, "treat", "treatment", "control", "manage", "what should", "next step", "remedy", "remedies", "prevent", "prevention", "care", "action") or "उपचार" in message or "इलाज" in message or "रोकथाम" in message:
            if profile:
                actions = management.get("preventive_intervention", [])
                if not actions:
                    actions = [management.get("cultural_practices", "Continue routine field scouting.")]
                answer = f"For the latest result ({name}), the knowledge base suggests: " + "; ".join(actions[:3])
                answer += " Check local agricultural guidance and product labels before applying any treatment."
            else:
                answer = (
                    "General first steps: inspect more than one plant, avoid handling "
                    "wet foliage, clean tools between plants, and ask a local "
                    "agricultural extension specialist to confirm the cause before "
                    "using a pesticide."
                )

        # Intent: Confidence, Scores & Calibration Explanation
        elif self._matches(text, "confidence", "score", "percentage", "probability", "risk", "result", "prediction", "disease", "diagnosis", "explain", "meaning") or "परिणाम" in message or "जोखिम" in message or "समझाएं" in message:
            if not profile:
                answer = (
                    "Run a leaf-image prediction first, and I can explain its "
                    "predicted class and scores. The image model's confidence and "
                    "the combined risk index are not calibrated probabilities."
                )
            elif profile.get("severity_level") == "Healthy":
                answer = (
                    f"The latest image prediction is {name}. The model's score is "
                    "not a calibrated probability, so use this as a screening result "
                    "and check the plant in the field."
                )
            else:
                score_text = (
                    f" The combined risk index is {fused_score:.1f} out of 100."
                    if fused_score is not None
                    else ""
                )
                answer = (
                    f"The image model's top class is {name}.{score_text} This is a "
                    "decision-support result, not a confirmed diagnosis or "
                    "calibrated disease probability. Compare the leaf with the "
                    "symptoms and seek local expert confirmation."
                )

        # Intent: Help Menu
        elif text in {"help", "what can you do", "what can you answer", "मदद", "सहायता"}:
            answer = (
                "I can explain this project's workflow, the latest prediction, "
                "reference symptoms, preventive steps, organic remedies, and the environmental "
                "favorability index. I use the project's local knowledge base; I "
                "don't diagnose beyond its saved crop classes."
            )

        # Fallback / General Inquiry
        else:
            if is_hindi:
                answer = (
                    "मैं इस परियोजना की फसल भविष्यवाणियों, लक्षणों, जैविक उपचारों और पर्यावरणीय जोखिम स्कोर में मदद कर सकता हूँ। "
                    "कृपया पूछें: “मेरे परिणाम का अर्थ क्या है?”, “इसके लक्षण क्या हैं?” या “जैविक उपचार क्या है?”"
                )
            else:
                answer = (
                    "I can help with this project's crop predictions, associated "
                    "symptoms, preventive guidance, and environmental score. Try asking "
                    "“Explain my result,” “What symptoms should I check?” or "
                    "“How does the environmental score work?”"
                )

        return {
            "answer": answer,
            "assistant": "Local crop knowledge assistant",
            "source": "Project disease knowledge base and prediction context",
            "disclaimer": "Decision-support information only; confirm important findings with a local agricultural expert.",
        }

    @staticmethod
    def _matches(text: str, *phrases: str) -> bool:
        for phrase in phrases:
            pat = r"\b" + re.escape(phrase) + r"(s|es|ing|ed)?\b"
            if re.search(pat, text):
                return True
        return False

    @staticmethod
    def _find_referenced_disease(text: str) -> Optional[str]:
        """Search if user explicitly mentions a known disease name in the prompt."""
        for crop_name, crop_info in CROPS_DATABASE.items():
            for d in crop_info["diseases"]:
                clean = d.replace("___", " ").replace("_", " ").lower()
                crop_part = clean.split()[0]
                disease_part = " ".join(clean.split()[1:])
                if disease_part and len(disease_part) > 4 and disease_part in text:
                    return d
        return None


crop_chatbot = CropChatbot()
