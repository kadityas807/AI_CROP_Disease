"""
CropPulse AI - Chatbot Neural Intent & Semantic Retrieval Model Training Pipeline
Trains a lightweight, high-accuracy PyTorch neural network on the 500-question agronomic dataset.
Outputs: models/chatbot_model.pth
"""

import sys
import json
import math
import random
import re
from pathlib import Path
from collections import Counter

import torch
import torch.nn as nn
import torch.nn.functional as F

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_PATH = PROJECT_ROOT / "backend" / "database" / "chatbot_500_qa.json"
if not DATA_PATH.exists():
    DATA_PATH = PROJECT_ROOT / "data" / "chatbot_500_qa.json"
MODEL_SAVE_PATH = PROJECT_ROOT / "models" / "chatbot_model.pth"


# -------------------------------------------------------------------------
# 1. Bilingual Text Preprocessing & Subword/Word Vectorizer
# -------------------------------------------------------------------------
def clean_text(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[?!.,;:\'\"()\[\]{}/\\<>+=_~`@#$%^&*|\-]", " ", t)
    return " ".join(t.split())


class ChatbotVectorizer:
    def __init__(self, max_features: int = 3500):
        self.max_features = max_features
        self.vocab = {}
        self.idf = None

    def _extract_ngrams(self, text: str):
        cleaned = clean_text(text)
        words = cleaned.split()
        tokens = []
        # Word unigrams
        tokens.extend(words)
        # Word bigrams
        for i in range(len(words) - 1):
            tokens.append(f"{words[i]}_{words[i+1]}")
        # Character 3-grams & 4-grams for subword matching (crucial for typos and Hindi)
        for w in words:
            if len(w) >= 3:
                for j in range(len(w) - 2):
                    tokens.append(f"c3:{w[j:j+3]}")
            if len(w) >= 4:
                for j in range(len(w) - 3):
                    tokens.append(f"c4:{w[j:j+4]}")
        return tokens

    def fit(self, texts):
        df = Counter()
        total_docs = len(texts)
        for t in texts:
            unique_tokens = set(self._extract_ngrams(t))
            for tok in unique_tokens:
                df[tok] += 1

        # Select top max_features by frequency
        most_common = df.most_common(self.max_features)
        self.vocab = {tok: idx for idx, (tok, _) in enumerate(most_common)}

        # Compute smoothed IDF
        idf_vec = torch.zeros(len(self.vocab), dtype=torch.float32)
        for tok, idx in self.vocab.items():
            count = df[tok]
            idf_vec[idx] = math.log((total_docs + 1.0) / (count + 1.0)) + 1.0
        self.idf = idf_vec

    def transform(self, texts):
        batch_size = len(texts)
        vecs = torch.zeros((batch_size, len(self.vocab)), dtype=torch.float32)
        for i, t in enumerate(texts):
            tokens = self._extract_ngrams(t)
            counts = Counter(tokens)
            for tok, cnt in counts.items():
                if tok in self.vocab:
                    idx = self.vocab[tok]
                    tf = 1.0 + math.log(cnt)
                    vecs[i, idx] = tf * self.idf[idx]

            # L2 normalization
            norm = torch.norm(vecs[i], p=2)
            if norm > 1e-6:
                vecs[i] /= norm
        return vecs


# -------------------------------------------------------------------------
# 2. PyTorch Neural Intent & Semantic Embedding Architecture
# -------------------------------------------------------------------------
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


# -------------------------------------------------------------------------
# 3. Data Augmentation for Robust Conversational Generalization
# -------------------------------------------------------------------------
def generate_training_variations(qas):
    train_texts = []
    train_labels = []

    prefixes = [
        "", "can you tell me ", "what is ", "explain ", "how to ", "how do I ",
        "tell me about ", "please help with ", "guide on "
    ]
    hindi_prefixes = ["", "कृपया बताएं ", "क्या आप बता सकते हैं ", "जानकारी दें "]

    for idx, item in enumerate(qas):
        q = item["question"]
        lang = item.get("language", "en")
        keywords = item.get("keywords", [])

        # 1. Exact question
        train_texts.append(q)
        train_labels.append(idx)

        # 2. Lowercase version
        train_texts.append(q.lower())
        train_labels.append(idx)

        # 3. Stripped question mark
        train_texts.append(q.rstrip("?").strip())
        train_labels.append(idx)

        # 4. Keyword query
        if keywords:
            kw_query = " ".join(keywords)
            train_texts.append(kw_query)
            train_labels.append(idx)

        # 5. Question rephrasing with conversational prefix
        cleaned = clean_text(q)
        words = cleaned.split()
        if len(words) > 3:
            core = " ".join(words[2:])
            if lang == "hi":
                p = random.choice(hindi_prefixes)
                train_texts.append(p + core)
            else:
                p = random.choice(prefixes)
                train_texts.append(p + core)
            train_labels.append(idx)

    return train_texts, train_labels


# -------------------------------------------------------------------------
# 4. Main Training Routine
# -------------------------------------------------------------------------
def train_chatbot():
    print(f"Loading 500 Q&A dataset from {DATA_PATH}...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        qas = json.load(f)

    num_classes = len(qas)
    print(f"Loaded {num_classes} canonical questions.")

    # Generate augmented training samples
    print("Generating training variations & query augmentations...")
    train_texts, train_labels = generate_training_variations(qas)
    print(f"Total augmented training examples: {len(train_texts)}")

    # Fit vectorizer
    print("Fitting subword & word n-gram TF-IDF vectorizer...")
    vectorizer = ChatbotVectorizer(max_features=3500)
    vectorizer.fit(train_texts)
    input_dim = len(vectorizer.vocab)
    print(f"Vocabulary size: {input_dim} features")

    # Transform all training texts
    X_train = vectorizer.transform(train_texts)
    y_train = torch.tensor(train_labels, dtype=torch.long)

    # Initialize PyTorch Model
    device = torch.device("cpu")
    model = ChatbotNeuralNet(
        input_dim=input_dim,
        hidden_dim=256,
        embed_dim=128,
        num_classes=num_classes
    ).to(device)

    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.0035, weight_decay=1e-4)

    epochs = 35
    batch_size = 64
    dataset_size = len(train_texts)
    steps_per_epoch = math.ceil(dataset_size / batch_size)

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    print("\nStarting Neural Intent & Semantic Model Training:")
    print("-" * 65)

    indices = list(range(dataset_size))
    for epoch in range(1, epochs + 1):
        model.train()
        random.shuffle(indices)
        total_loss = 0.0
        correct = 0

        for s in range(steps_per_epoch):
            batch_idx = indices[s * batch_size : (s + 1) * batch_size]
            bx = X_train[batch_idx].to(device)
            by = y_train[batch_idx].to(device)

            optimizer.zero_grad()
            logits, _ = model(bx)
            loss = criterion(logits, by)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * len(batch_idx)
            preds = logits.argmax(dim=-1)
            correct += (preds == by).sum().item()

        scheduler.step()
        epoch_loss = total_loss / dataset_size
        epoch_acc = (correct / dataset_size) * 100.0

        if epoch % 5 == 0 or epoch == 1 or epoch == epochs:
            print(f"Epoch {epoch:2d}/{epochs:2d} | Loss: {epoch_loss:.4f} | Training Accuracy: {epoch_acc:6.2f}%")

    print("-" * 65)
    print("Training complete! Evaluating Top-1 and Top-3 accuracy on canonical 500 questions...")

    # Evaluation on the exact 500 questions
    model.eval()
    with torch.no_grad():
        canonical_texts = [item["question"] for item in qas]
        X_canon = vectorizer.transform(canonical_texts).to(device)
        logits, embeds = model(X_canon)
        top1 = (logits.argmax(dim=-1) == torch.arange(num_classes)).sum().item()
        top3_preds = logits.topk(3, dim=-1).indices
        top3 = sum(i in top3_preds[i] for i in range(num_classes))

        top1_acc = (top1 / num_classes) * 100.0
        top3_acc = (top3 / num_classes) * 100.0
        print(f"Top-1 Retrieval Accuracy: {top1_acc:.2f}% ({top1}/{num_classes})")
        print(f"Top-3 Retrieval Accuracy: {top3_acc:.2f}% ({top3}/{num_classes})")

        # Pre-compute and normalize 128-dim embeddings for all 500 target questions
        norm_question_embeddings = F.normalize(embeds, p=2, dim=-1)

    # Save model checkpoint and assets
    checkpoint = {
        "model_state_dict": model.state_dict(),
        "input_dim": input_dim,
        "hidden_dim": 256,
        "embed_dim": 128,
        "num_classes": num_classes,
        "vocab": vectorizer.vocab,
        "idf": vectorizer.idf,
        "qas": qas,
        "question_embeddings": norm_question_embeddings.cpu()
    }

    MODEL_SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(checkpoint, MODEL_SAVE_PATH)
    file_size_mb = MODEL_SAVE_PATH.stat().st_size / (1024 * 1024)
    print(f"\nModel successfully saved to {MODEL_SAVE_PATH} ({file_size_mb:.2f} MB)")
    print("Chatbot is now fully trained and ready for real-time inference!")


if __name__ == "__main__":
    train_chatbot()
