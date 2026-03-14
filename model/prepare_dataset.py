"""
model/prepare_dataset.py
─────────────────────────
Prepares the Kaggle ISL dataset (prathumarikeri) for training.

The downloaded dataset has this structure:
  indian/
    1/   2/   ...  9/
    a/   b/   ...  z/

This script:
  1. Renames numeric folders 1-9 → One, Two, ... Nine
     (so class names are readable words, not digits)
  2. Copies everything into data/raw/images/ with clean names
  3. Prints a summary of class sizes

Usage:
  python model/prepare_dataset.py --src /path/to/indian

  # Example if dataset is in Downloads:
  python model/prepare_dataset.py --src ~/Downloads/indian
"""

import os
import sys
import shutil
import argparse

# Map digit folder names → English word class names
DIGIT_MAP = {
    "1": "One",   "2": "Two",   "3": "Three",
    "4": "Four",  "5": "Five",  "6": "Six",
    "7": "Seven", "8": "Eight", "9": "Nine"
}

# Map letter folders → uppercase (a → A, b → B, ...)
def letter_name(folder: str) -> str:
    return folder.upper() if len(folder) == 1 and folder.isalpha() else folder


def prepare(src_dir: str, out_dir: str):
    if not os.path.isdir(src_dir):
        print(f"[ERROR] Source directory not found: {src_dir}")
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)
    folders = sorted(os.listdir(src_dir))
    total_images = 0

    print(f"\nPreparing dataset from: {src_dir}")
    print(f"Output directory:       {out_dir}\n")
    print(f"{'Folder':<10} {'Class name':<12} {'Images':>8}")
    print("-" * 34)

    for folder in folders:
        src_cls = os.path.join(src_dir, folder)
        if not os.path.isdir(src_cls):
            continue

        # Determine clean class name
        if folder in DIGIT_MAP:
            class_name = DIGIT_MAP[folder]
        else:
            class_name = letter_name(folder)

        dst_cls = os.path.join(out_dir, class_name)
        os.makedirs(dst_cls, exist_ok=True)

        images = [f for f in os.listdir(src_cls)
                  if f.lower().endswith((".jpg", ".jpeg", ".png"))]

        for fname in images:
            shutil.copy2(
                os.path.join(src_cls, fname),
                os.path.join(dst_cls, fname)
            )

        print(f"{folder:<10} {class_name:<12} {len(images):>8}")
        total_images += len(images)

    print("-" * 34)
    print(f"{'TOTAL':<22} {total_images:>8} images")
    print(f"\nDataset ready at: {out_dir}")
    print("\nNext steps:")
    print("  python model/extract_landmarks.py --mode image --src data/raw/images")
    print("  python model/train_lstm.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True,
                        help="Path to the downloaded 'indian' folder from Kaggle")
    parser.add_argument("--out", default="data/raw/images",
                        help="Output path for prepared dataset (default: data/raw/images)")
    args = parser.parse_args()
    prepare(os.path.expanduser(args.src), args.out)
