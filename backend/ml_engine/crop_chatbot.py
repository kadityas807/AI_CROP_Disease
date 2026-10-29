"""Local, knowledge-base-backed crop help chatbot."""

import re
from typing import Optional

from backend.database.knowledge_base import get_disease_profile


class CropChatbot:
    def answer(
        self,
        message: str,
        predicted_class: Optional[str] = None,
        environmental_score: Optional[float] = None,
        fused_score: Optional[float] = None,
    ) -> dict:
        text = message.lower().strip()
        profile = get_disease_profile(predicted_class) if predicted_class else None
        name = profile["common_name"] if profile else None

        if self._matches(text, "hello", "hi", "hey", "good morning", "good afternoon"):
            answer = (
                "Hello! I can explain your leaf prediction, symptoms, environmental "
                "score, and preventive guidance. Try asking “Explain my result” or "
                "“What should I do next?”"
            )
        elif self._matches(text, "how does", "how do", "how it work", "how this work", "workflow", "project work"):
            answer = (
                "Upload a leaf photo and choose its crop. The MobileNetV2 image model "
                "ranks likely leaf classes. The app separately calculates a "
                "rule-based environmental favorability index, then combines those "
                "signals into a decision-support score and displays guidance."
            )
        elif self._matches(text, "weather", "humidity", "rainfall", "leaf wetness", "temperature", "environment"):
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
        elif self._matches(text, "confidence", "score", "percentage", "probability", "risk", "result", "prediction", "disease", "diagnosis", "explain"):
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
        elif self._matches(text, "symptom", "symptoms", "look like", "sign", "signs", "identify", "spot", "lesion"):
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
        elif self._matches(text, "treat", "treatment", "control", "manage", "what should", "next step", "remedy", "remedies", "prevent", "prevention", "care"):
            if profile:
                management = profile.get("management", {})
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
        elif text in {"help", "what can you do", "what can you answer"}:
            answer = (
                "I can explain this project's workflow, the latest prediction, "
                "reference symptoms, preventive steps, and the environmental "
                "favorability index. I use the project's local knowledge base; I "
                "don't diagnose beyond its saved crop classes."
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
        return any(
            re.search(rf"\b{re.escape(phrase)}\b", text)
            for phrase in phrases
        )


crop_chatbot = CropChatbot()
