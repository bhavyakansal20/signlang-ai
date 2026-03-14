FROM python:3.11-slim

WORKDIR /app

# System libraries needed by OpenCV + MediaPipe
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libusb-1.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
```

---

## Step 4 — Add secrets on Hugging Face

Your app needs `APPS_SCRIPT_URL` and `SECRET_KEY` — don't hardcode them.

1. Go to your Space → **Settings** tab
2. Scroll to **Variables and secrets**
3. Click **New secret** and add:
```
APPS_SCRIPT_URL = https://script.google.com/macros/s/your-url/exec
SECRET_KEY      = any-long-random-string-here
