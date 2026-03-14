# ── SignLang AI — Dockerfile ──────────────────────────────────
# Target: Hugging Face Spaces (CPU, port 7860)
# Base:   Python 3.11 slim

FROM python:3.11-slim

# System dependencies required by OpenCV + MediaPipe
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Install Python dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Create directories that must exist at runtime
RUN mkdir -p data/landmarks model/plots static/audio

# HuggingFace Spaces: run as non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose port (HF Spaces requires 7860)
EXPOSE 7860

# Environment defaults (override via HF Spaces secrets)
ENV SECRET_KEY="signlang-ai-hf-2026"
ENV PYTHONUNBUFFERED=1

# Launch Flask
CMD ["python", "app.py"]
