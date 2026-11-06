"""
Local agronomic knowledge assistant for crop health decision support.
Trained on 500 comprehensive agronomic & platform Q&As using a PyTorch neural semantic retrieval network.
Grounds responses in the 41-class disease knowledge base, microclimate triggers,
integrated pest management (IPM) guidance, and CIBRC safety rules in English and Hindi.
"""

import math
import re
from collections import Counter
from pathlib import Path
from typing import Optional, Dict, Any, List

import torch
import torch.nn as nn
import torch.nn.functional as F

from backend.database.knowledge_base import get_disease_profile, CROPS_DATABASE

MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "chatbot_model.pth"


class ChatbotNeuralNet(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 256, embed_dim: int = 128, num_classes: int = 500):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.norm1 = nn.LayerNorm(hidden_dim)
        self.act = nn.GELU()
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(hidden_dim, embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, num_classes)

    def forward(self, x):
        h = self.act(self.norm1(self.fc1(x)))
        h = self.dropout(h)
        embed = self.norm2(self.fc2(h))
        logits = self.head(embed)
        return logits, embed

    def get_embedding(self, x):
        h = self.act(self.norm1(self.fc1(x)))
        embed = self.norm2(self.fc2(h))
        return F.normalize(embed, p=2, dim=-1)


def clean_text(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[?!.,;:\'\"()\[\]{}/\\<>+=_~`@#$%^&*|\-]", " ", t)
    return " ".join(t.split())


class CropChatbot:
    def __init__(self):
        self.is_trained = False
        self.model = None
        self.vocab = {}
        self.idf = None
        self.qas = []
        self.q_embeds = None
        self._load_model()

    def _load_model(self):
        if not MODEL_PATH.exists():
            return
        try:
            ckpt = torch.load(MODEL_PATH, map_location="cpu")
            self.vocab = ckpt["vocab"]
            self.idf = ckpt["idf"]
            self.qas = ckpt["qas"]
            self.q_embeds = ckpt["question_embeddings"]
            input_dim = ckpt["input_dim"]
            num_classes = ckpt["num_classes"]

            self.model = ChatbotNeuralNet(
                input_dim=input_dim,
                hidden_dim=256,
                embed_dim=128,
                num_classes=num_classes
            )
            self.model.load_state_dict(ckpt["model_state_dict"])
            self.model.eval()
            self.is_trained = True
        except Exception as e:
            print(f"Warning: Failed to load trained chatbot model: {e}")

    def _vectorize(self, query: str) -> torch.Tensor:
        cleaned = clean_text(query)
        words = cleaned.split()
        tokens = list(words)
        for i in range(len(words) - 1):
            tokens.append(f"{words[i]}_{words[i+1]}")
        for w in words:
            if len(w) >= 3:
                for j in range(len(w) - 2):
                    tokens.append(f"c3:{w[j:j+3]}")
            if len(w) >= 4:
                for j in range(len(w) - 3):
                    tokens.append(f"c4:{w[j:j+4]}")

        vec = torch.zeros((1, len(self.vocab)), dtype=torch.float32)
        counts = Counter(tokens)
        for tok, cnt in counts.items():
            if tok in self.vocab:
                idx = self.vocab[tok]
                vec[0, idx] = (1.0 + math.log(cnt)) * self.idf[idx]
        norm = torch.norm(vec, p=2)
        if norm > 1e-6:
            vec /= norm
        return vec

    def _neural_search(self, query: str):
        if not self.is_trained or not self.model or self.q_embeds is None:
            return None, 0.0

        vec = self._vectorize(query)
        with torch.no_grad():
            logits, _ = self.model(vec)
            query_embed = self.model.get_embedding(vec)
            sims = torch.mm(query_embed, self.q_embeds.t()).squeeze(0)
            probs = F.softmax(logits, dim=-1).squeeze(0)

            combined = 0.5 * probs + 0.5 * sims
            best_idx = combined.argmax().item()
            best_score = combined[best_idx].item()
            return self.qas[best_idx], best_score

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

        referenced_class = self._find_referenced_disease(text)
        active_class = referenced_class or predicted_class
        profile = get_disease_profile(active_class) if active_class else None

        name = profile["common_name"] if profile else None
        management = profile.get("management", {}) if profile else {}

        # 1. Multi-turn scan context: If user asks about their active scan (without naming another disease)
        is_generic_scan_symptom_query = (
            predicted_class is not None and not referenced_class and
            self._matches(text, "symptom", "look like", "sign", "identify")
        )
        if is_generic_scan_symptom_query and profile:
            symptoms = profile.get("symptoms", [])
            answer = f"Symptoms associated with {name} include: " + "; ".join(symptoms[:4])
            answer += " These are reference symptoms, not proof that the plant has this disease."
            return self._format_response(answer)

        is_generic_scan_action_query = (
            predicted_class is not None and not referenced_class and
            self._matches(text, "what should i do", "what to do", "next step", "what should we do")
        )
        if is_generic_scan_action_query and profile:
            actions = management.get("preventive_intervention", [])
            if not actions:
                actions = [management.get("cultural_practices", "Continue routine field scouting.")]
            answer = f"For the latest result ({name}), the knowledge base suggests: " + "; ".join(actions[:3])
            answer += " Check local agricultural guidance and product labels before applying any treatment."
            return self._format_response(answer)

        is_generic_scan_score_query = (
            fused_score is not None and
            self._matches(text, "explain my result", "explain the score", "explain result", "score meaning", "risk index")
        )
        if is_generic_scan_score_query and profile:
            score_text = f" The combined risk index is {fused_score:.1f} out of 100."
            answer = (
                f"The image model's top class is {name}.{score_text} This is a "
                "decision-support result, not a confirmed diagnosis or "
                "calibrated disease probability. Compare the leaf with the "
                "symptoms and seek local expert confirmation."
            )
            return self._format_response(answer)

        # 2. Neural Retrieval across the 500 Trained Agronomic Questions
        match, score = self._neural_search(message)
        if match and score >= 0.20:
            return self._format_response(match["answer"])

        # 3. Fallbacks
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
        elif self._matches(text, "how does", "how do", "how it work", "how this work", "workflow", "project work", "architecture") or "काम कैसे" in message or "प्रणाली" in message:
            answer = (
                "Upload a leaf photo and choose its crop. The MobileNetV2 image model "
                "ranks likely leaf classes across 41 canonical plant diseases. The app separately calculates a "
                "rule-based environmental favorability index based on microclimate telemetry (temperature, humidity, leaf wetness, rainfall), "
                "then combines those signals into a decision-support score and displays IPM guidance."
            )
        elif self._matches(text, "symptom", "sign", "look like") or "लक्षण" in message:
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

        return self._format_response(answer)

    @staticmethod
    def _format_response(answer: str) -> dict:
        return {
            "answer": answer,
            "assistant": "Local crop knowledge assistant",
            "source": "Trained 500 Q&A neural model & disease knowledge base",
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
        for crop_name, crop_info in CROPS_DATABASE.items():
            for d in crop_info["diseases"]:
                clean = d.replace("___", " ").replace("_", " ").lower()
                crop_part = clean.split()[0]
                disease_part = " ".join(clean.split()[1:])
                if disease_part and len(disease_part) > 4 and disease_part in text:
                    return d
        return None


crop_chatbot = CropChatbot()
