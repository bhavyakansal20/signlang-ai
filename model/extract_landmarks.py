"""
model/extract_landmarks.py
──────────────────────────
Converts raw dataset images/videos into MediaPipe landmark .npy files.

Supports:
  - Image dataset  (e.g. Kaggle ISL A-Z — one image per gesture)
  - Video dataset  (e.g. INCLUDE-50 — one video per gesture sequence)

Usage:
  # For image dataset (Kaggle ISL):
  python model/extract_landmarks.py --mode image --src data/raw/images

  # For video dataset (INCLUDE-50):
  python model/extract_landmarks.py --mode video --src data/raw/videos

Expected input structure:
  data/raw/images/
    A/  img001.jpg img002.jpg ...
    B/  ...
    Hello/  ...

  data/raw/videos/
    Hello/  vid001.mp4 vid002.mp4 ...
    ThankYou/ ...

Output:
  data/landmarks/
    A/  seq_001.npy  ← shape: (30, 63) — 30 copies of same frame landmark
    Hello/  seq_001.npy  ← shape: (N_frames, 63)
"""

import os
import sys
import argparse
import numpy as np
import cv2

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.landmark_extractor import LandmarkExtractor

extractor = LandmarkExtractor()

SEQ_LEN = 30


def process_image_dataset(src_dir: str, out_dir: str):
    """
    For each class folder in src_dir, extract one landmark frame per image
    and replicate it SEQ_LEN times to create a (30, 63) sequence.
    This makes image data compatible with the LSTM's sequence input.
    """
    classes = sorted([d for d in os.listdir(src_dir)
                      if os.path.isdir(os.path.join(src_dir, d))])
    print(f"[Extract] Found {len(classes)} classes in {src_dir}")

    for cls in classes:
        cls_in  = os.path.join(src_dir, cls)
        cls_out = os.path.join(out_dir, cls)
        os.makedirs(cls_out, exist_ok=True)
        images  = [f for f in os.listdir(cls_in)
                   if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        saved = 0
        for i, fname in enumerate(images):
            img = cv2.imread(os.path.join(cls_in, fname))
            if img is None:
                continue
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            lm, _ = extractor.extract(rgb, img.copy())
            if lm is None:
                continue
            # Replicate single frame to make a sequence
            sequence = np.tile(lm, (SEQ_LEN, 1))  # (30, 63)
            np.save(os.path.join(cls_out, f"seq_{i:04d}.npy"), sequence)
            saved += 1
        print(f"  [{cls}] {saved}/{len(images)} images → landmark sequences")


def process_video_dataset(src_dir: str, out_dir: str):
    """
    For each video in each class folder, extract frame-by-frame landmarks.
    Saves as (N_frames, 63) where N_frames is the number of frames
    with a detected hand.
    """
    classes = sorted([d for d in os.listdir(src_dir)
                      if os.path.isdir(os.path.join(src_dir, d))])
    print(f"[Extract] Found {len(classes)} classes in {src_dir}")

    for cls in classes:
        cls_in  = os.path.join(src_dir, cls)
        cls_out = os.path.join(out_dir, cls)
        os.makedirs(cls_out, exist_ok=True)
        videos  = [f for f in os.listdir(cls_in)
                   if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))]
        saved = 0
        for i, fname in enumerate(videos):
            cap    = cv2.VideoCapture(os.path.join(cls_in, fname))
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                lm, _ = extractor.extract(rgb, frame.copy())
                if lm is not None:
                    frames.append(lm)
            cap.release()

            if len(frames) < SEQ_LEN // 2:
                continue  # Skip very short sequences

            sequence = np.array(frames, dtype=np.float32)  # (N_frames, 63)
            np.save(os.path.join(cls_out, f"seq_{i:04d}.npy"), sequence)
            saved += 1
        print(f"  [{cls}] {saved}/{len(videos)} videos → landmark sequences")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["image", "video"], default="image",
                        help="Dataset type: image (Kaggle ISL) or video (INCLUDE-50)")
    parser.add_argument("--src",  default="data/raw/images",
                        help="Path to raw dataset folder")
    parser.add_argument("--out",  default="data/landmarks",
                        help="Output folder for landmark .npy files")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    if args.mode == "image":
        process_image_dataset(args.src, args.out)
    else:
        process_video_dataset(args.src, args.out)

    print("[Extract] Done. Now run: python model/train_lstm.py")
