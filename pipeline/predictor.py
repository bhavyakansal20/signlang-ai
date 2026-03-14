"""pipeline/predictor.py — LSTM inference engine."""

import json
import numpy as np
import torch
import torch.nn as nn
from collections import deque


# ── Model Definition ──────────────────────────────────────────
class SignLSTM(nn.Module):
    """
    3-layer LSTM for gesture sequence classification.
    Input:  (batch, seq_len=30, features=63)
    Output: (batch, num_classes)
    """
    def __init__(self, input_size=63, hidden_size=128,
                 num_layers=3, num_classes=50, dropout=0.3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.dropout = nn.Dropout(dropout)
        self.fc1     = nn.Linear(hidden_size, 64)
        self.relu    = nn.ReLU()
        self.fc2     = nn.Linear(64, num_classes)

    def forward(self, x):
        out, _ = self.lstm(x)      # (batch, seq, hidden)
        out     = out[:, -1, :]    # last timestep
        out     = self.dropout(out)
        out     = self.relu(self.fc1(out))
        return self.fc2(out)


# ── Predictor ─────────────────────────────────────────────────
class GesturePredictor:
    """
    Loads a trained SignLSTM model and runs inference.
    Uses a majority-vote buffer over last N predictions for stability.
    """

    def __init__(self, model_path: str, label_map_path: str,
                 vote_window: int = 5, confidence_threshold: float = 0.70):
        self.confidence_threshold = confidence_threshold
        self.vote_buffer = deque(maxlen=vote_window)
        self.device      = torch.device("cpu")

        # ── Load label map ────────────────────────────────────
        try:
            with open(label_map_path) as f:
                raw_map  = json.load(f)
            # label_map: {class_index_str: word_string}
            self.label_map = {int(k): v for k, v in raw_map.items()}
            num_classes    = len(self.label_map)
        except FileNotFoundError:
            print(f"[Predictor] label_map.json not found at {label_map_path}. "
                  "Using demo mode with 50 dummy classes.")
            num_classes    = 50
            self.label_map = {i: f"Sign_{i}" for i in range(50)}

        # ── Load model ────────────────────────────────────────
        self.model = SignLSTM(input_size=63, hidden_size=128,
                              num_layers=3, num_classes=num_classes)
        try:
            state = torch.load(model_path, map_location=self.device,
                               weights_only=True)
            self.model.load_state_dict(state)
            self.model.eval()
            print(f"[Predictor] Model loaded from {model_path}")
        except FileNotFoundError:
            print(f"[Predictor] Model not found at {model_path}. "
                  "Running in DEMO mode — train the model first using model/train_lstm.py")
            self.model = None

    def predict(self, sequence: np.ndarray):
        """
        sequence: np.ndarray of shape (30, 63)
        Returns: (word: str, confidence: float) or ("", 0.0)
        """
        if self.model is None:
            return "", 0.0

        x = torch.tensor(sequence, dtype=torch.float32).unsqueeze(0)  # (1, 30, 63)

        with torch.no_grad():
            logits = self.model(x)
            probs  = torch.softmax(logits, dim=1).squeeze()
            conf, idx = torch.max(probs, dim=0)
            conf  = conf.item()
            idx   = idx.item()

        if conf < self.confidence_threshold:
            return "", conf

        word = self.label_map.get(idx, "Unknown")
        self.vote_buffer.append(word)

        # Majority vote
        if len(self.vote_buffer) == self.vote_buffer.maxlen:
            from collections import Counter
            voted = Counter(self.vote_buffer).most_common(1)[0][0]
            return voted, conf

        return word, conf
