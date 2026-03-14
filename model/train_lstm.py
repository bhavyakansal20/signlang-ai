"""
model/train_lstm.py
───────────────────
Full training pipeline for SignLang AI's gesture recognition model.

Steps:
  1. Reads pre-extracted landmark .npy files from data/landmarks/
  2. Builds PyTorch dataset with 30-frame sliding windows
  3. Trains 3-layer LSTM with dropout
  4. Saves model as signlang_model.pt and label_map.json
  5. Plots and saves accuracy + loss curves

Run:  python model/train_lstm.py

Before running, extract landmarks using:
  python model/extract_landmarks.py
"""

import os
import sys
import json
import model
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from sklearn.preprocessing import LabelEncoder
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tqdm import tqdm

# ── Add project root to path ──────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.predictor import SignLSTM

# ── Config ────────────────────────────────────────────────────
LANDMARKS_DIR = "data/landmarks"   # Each .npy file is (N_frames, 63)
MODEL_OUT     = "model/signlang_model.pt"
LABEL_MAP_OUT = "model/label_map.json"
PLOTS_DIR     = "model/plots"
SEQ_LEN       = 30       # frames per sequence
BATCH_SIZE    = 32
EPOCHS        = 60
LR            = 1e-3
HIDDEN_SIZE   = 128
NUM_LAYERS    = 3
DROPOUT       = 0.3
TRAIN_SPLIT   = 0.85
DEVICE        = torch.device("mps" if torch.backends.mps.is_available()
                              else "cuda" if torch.cuda.is_available()
                              else "cpu")
print(f"[Train] Using device: {DEVICE}")
os.makedirs(PLOTS_DIR, exist_ok=True)


# ── Dataset ───────────────────────────────────────────────────
class GestureDataset(Dataset):
    """
    Loads per-class landmark sequences from data/landmarks/.
    Folder structure expected:
      data/landmarks/
        Hello/          ← class name is the folder name
          seq_001.npy   ← shape: (N_frames, 63)  where N_frames >= SEQ_LEN
          seq_002.npy
        ThankYou/
          ...

    If a sequence has > SEQ_LEN frames, uses a sliding window
    to produce multiple training samples.
    """

    def __init__(self, landmarks_dir: str, seq_len: int = 30):
        self.seq_len  = seq_len
        self.samples  = []   # list of (sequence np.ndarray shape [seq_len, 63], label_idx)
        self.classes  = []
        self.encoder  = LabelEncoder()

        class_names = sorted([
            d for d in os.listdir(landmarks_dir)
            if os.path.isdir(os.path.join(landmarks_dir, d))
        ])

        if not class_names:
            raise RuntimeError(
                f"No class folders found in {landmarks_dir}.\n"
                "Run model/extract_landmarks.py first to generate landmark files."
            )

        self.encoder.fit(class_names)
        self.classes = class_names

        for cls in class_names:
            cls_dir = os.path.join(landmarks_dir, cls)
            label   = self.encoder.transform([cls])[0]
            for fname in os.listdir(cls_dir):
                if not fname.endswith(".npy"):
                    continue
                data = np.load(os.path.join(cls_dir, fname)).astype(np.float32)
                # data shape: (N_frames, 63)
                if len(data) < seq_len:
                    # Pad with zeros if too short
                    pad  = np.zeros((seq_len - len(data), 63), dtype=np.float32)
                    data = np.vstack([data, pad])
                # Sliding window
                for start in range(0, len(data) - seq_len + 1, seq_len // 2):
                    window = data[start: start + seq_len]
                    self.samples.append((window, label))

        print(f"[Dataset] {len(self.samples)} sequences across {len(class_names)} classes")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        seq, label = self.samples[idx]
        return torch.tensor(seq, dtype=torch.float32), torch.tensor(label, dtype=torch.long)


# ── Training ──────────────────────────────────────────────────
def train():
    # 1. Load dataset
    dataset     = GestureDataset(LANDMARKS_DIR, SEQ_LEN)
    num_classes = len(dataset.classes)
    n_train     = int(len(dataset) * TRAIN_SPLIT)
    n_val       = len(dataset) - n_train
    train_ds, val_ds = random_split(dataset, [n_train, n_val],
                                    generator=torch.Generator().manual_seed(42))

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=0)
    val_loader   = DataLoader(val_ds,   batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    print(f"[Train] Classes ({num_classes}): {dataset.classes}")
    print(f"[Train] Train: {n_train}  |  Val: {n_val}")

    # 2. Build model
    model     = SignLSTM(input_size=63, hidden_size=HIDDEN_SIZE,
                         num_layers=NUM_LAYERS, num_classes=num_classes,
                         dropout=DROPOUT).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.5)

    history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}
    best_val_acc = 0.0

    # 3. Epoch loop
    for epoch in range(1, EPOCHS + 1):
        # ── Train phase ───────────────────────────────────────
        model.train()
        t_loss, t_correct, t_total = 0.0, 0, 0
        for X, y in tqdm(train_loader, desc=f"Epoch {epoch}/{EPOCHS} [Train]", leave=False):
            X, y = X.to(DEVICE), y.to(DEVICE)
            optimizer.zero_grad()
            out  = model(X)
            loss = criterion(out, y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            t_loss    += loss.item() * X.size(0)
            preds      = out.argmax(dim=1)
            t_correct += (preds == y).sum().item()
            t_total   += X.size(0)

        # ── Val phase ─────────────────────────────────────────
        model.eval()
        v_loss, v_correct, v_total = 0.0, 0, 0
        with torch.no_grad():
            for X, y in val_loader:
                X, y  = X.to(DEVICE), y.to(DEVICE)
                out   = model(X)
                loss  = criterion(out, y)
                v_loss    += loss.item() * X.size(0)
                preds      = out.argmax(dim=1)
                v_correct += (preds == y).sum().item()
                v_total   += X.size(0)

        train_acc = t_correct / t_total * 100
        val_acc   = v_correct / v_total * 100
        train_loss = t_loss / t_total
        val_loss   = v_loss / v_total

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["train_acc"].append(train_acc)
        history["val_acc"].append(val_acc)

        scheduler.step()
        print(f"  Epoch {epoch:3d}/{EPOCHS}  "
              f"T_Loss: {train_loss:.4f}  T_Acc: {train_acc:.1f}%  |  "
              f"V_Loss: {val_loss:.4f}  V_Acc: {val_acc:.1f}%")

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), MODEL_OUT)
            print(f"  ✓ Best model saved — Val Acc: {best_val_acc:.1f}%")

    # 4. Save label map
    label_map = {int(i): cls for i, cls in enumerate(dataset.classes)}
    with open(LABEL_MAP_OUT, "w") as f:
        json.dump(label_map, f, indent=2)
    print(f"[Train] Label map saved → {LABEL_MAP_OUT}")

    # 5. Plot curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("SignLang AI — Training Curves", fontsize=14, fontweight="bold")

    ax1.plot(history["train_loss"], label="Train Loss", color="#7C3AED")
    ax1.plot(history["val_loss"],   label="Val Loss",   color="#0F6E56", linestyle="--")
    ax1.set_title("Loss");  ax1.set_xlabel("Epoch"); ax1.legend(); ax1.grid(alpha=0.3)

    ax2.plot(history["train_acc"], label="Train Acc", color="#7C3AED")
    ax2.plot(history["val_acc"],   label="Val Acc",   color="#0F6E56", linestyle="--")
    ax2.set_title("Accuracy (%)"); ax2.set_xlabel("Epoch"); ax2.legend(); ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "training_curves.png"), dpi=150)
    print(f"[Train] Plots saved → {PLOTS_DIR}/training_curves.png")
    print(f"\n[Train] Done. Best Val Accuracy: {best_val_acc:.1f}%")

    # training complete hone ke baad

torch.save(model.state_dict(), "model/sign_model.pth")
print("Model saved successfully")

if __name__ == "__main__":
    train()
