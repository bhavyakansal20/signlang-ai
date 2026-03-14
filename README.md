---
title: SignLang AI
emoji: 🤙
colorFrom: orange
colorTo: yellow
sdk: docker
pinned: false
---

<div align="center">

<br>

```
███████╗██╗ ██████╗ ███╗   ██╗██╗      █████╗ ███╗   ██╗ ██████╗      █████╗ ██╗
██╔════╝██║██╔════╝ ████╗  ██║██║     ██╔══██╗████╗  ██║██╔════╝     ██╔══██╗██║
███████╗██║██║  ███╗██╔██╗ ██║██║     ███████║██╔██╗ ██║██║  ███╗    ███████║██║
╚════██║██║██║   ██║██║╚██╗██║██║     ██╔══██║██║╚██╗██║██║   ██║    ██╔══██║██║
███████║██║╚██████╔╝██║ ╚████║███████╗██║  ██║██║ ╚████║╚██████╔╝    ██║  ██║██║
╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝  ╚═╝╚═╝
```

### ✦ Real-time Indian Sign Language Recognition — Powered by Deep Learning ✦
#### Every Hand Has a Voice. Break the Silence with AI.

<br>

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Visit%20Now-F0820F?style=for-the-badge&labelColor=07060A)](https://huggingface.co/spaces/BhavyaKansal20/SignLang-AI)
[![GitHub Repo](https://img.shields.io/badge/⭐%20GitHub-Star%20Repo-F0820F?style=for-the-badge&labelColor=07060A)](https://github.com/BhavyaKansal20/SignLang-AI)

<br>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.2-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-0097A7?style=flat-square&logo=google&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![gTTS](https://img.shields.io/badge/gTTS-2.5-34A853?style=flat-square&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black)

<br>

> **"7 crore Indians are deaf or hard of hearing. SignLang AI gives every one of them a voice — in real-time, through any webcam."**

</div>

---

<br>

## ⚡ At a Glance

<div align="center">

| ✋ Two-Hand Detection | 🧠 LSTM Model | 🎙️ Bilingual TTS | ✨ NLP Polish | 📖 Sign Dictionary |
|:---:|:---:|:---:|:---:|:---:|
| MediaPipe Dual Track | 3-Layer PyTorch | English + Hindi | Rule-based NLP | 35 ISL Signs |
| 21 landmarks × hand | 99.9% Val Acc | gTTS Engine | Auto grammar fix | Slide-up drawer |
| Both skeletons drawn | 42,000+ samples | Real-time speak | Sentence builder | Click to hear |

</div>

---

<br>

## 🏗️ System Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🤙  SIGNLANG AI  —  SYSTEM ARCHITECTURE                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   ┌─────────────┐     HTTPS      ┌──────────────────────────────────────┐   ║
║   │   🌐 USER   │ ─────────────► │          FLASK APPLICATION           │   ║
║   │   BROWSER   │                │                                      │   ║
║   └─────────────┘                │  ┌────────────┐  ┌────────────────┐  │   ║
║                                  │  │  Auth      │  │  Route Handler │  │   ║
║   ┌─────────────┐                │  │  Middleware │  │  /dashboard    │  │   ║
║   │  📷 WEBCAM  │ ─────────────► │  │  (SHA-256) │  │  /api/camera   │  │   ║
║   │   30 FPS    │                │  └────────────┘  │  /api/tts      │  │   ║
║   └─────────────┘                │                  │  /api/nlp      │  │   ║
║                                  └──────────────┬───└────────────────┘──┘   ║
║                                                 │                            ║
║        ┌────────────────────────────────────────┼────────────────────┐      ║
║        │                      │                 │                    │      ║
║        ▼                      ▼                 ▼                    ▼      ║
║  ┌───────────────┐  ┌──────────────────┐  ┌──────────┐  ┌─────────────────┐ ║
║  │ 📡 MEDIAPIPE  │  │  🧠 LSTM ENGINE  │  │ 🔤 NLP   │  │  🔊 TTS ENGINE  │ ║
║  │               │  │                  │  │  ENGINE  │  │                 │ ║
║  │  2-Hand track │  │  signlang_       │  │  Polish  │  │  gTTS English   │ ║
║  │  21 landmarks │  │  model.pt        │  │  Grammar │  │  gTTS Hindi     │ ║
║  │  per hand     │  │  label_map.json  │  │  Clean   │  │  deep-          │ ║
║  │  63 features  │  │  35 classes      │  │  Punct.  │  │  translator     │ ║
║  └───────────────┘  └──────────────────┘  └──────────┘  └─────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

<br>

## 🤖 ML Pipeline

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        ML PIPELINE — END TO END                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   RAW DATA               PREPROCESSING           LANDMARK EXTRACTION        ║
║  ──────────             ───────────────          ──────────────────────      ║
║  42,745 ISL  ─────────► Folder scan   ─────────► MediaPipe Hands            ║
║  images                 Class mapping            21 (x,y,z) landmarks       ║
║  35 classes             80/20 split              Wrist-normalized            ║
║                                                  63 features flat            ║
║                                                                              ║
║   SEQUENCE BUILD          MODEL TRAINING            INFERENCE                ║
║  ───────────────         ────────────────          ──────────               ║
║  30 frames/seq ────────► 3-layer LSTM   ─────────► Majority vote            ║
║  Sliding window          hidden=128               buffer (5 frames)         ║
║  Augmentation            dropout=0.3              conf threshold 0.70       ║
║                          60 epochs                35-class softmax          ║
║                          MPS (Apple M4)           → word + confidence       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

<br>

## 📊 Model Performance

<div align="center">

```
  SIGNLANG LSTM MODEL — TRAINING RESULTS
  ───────────────────────────────────────

  Val Accuracy   ████████████████████  99.9%   (Epoch 22 best)
  Train Accuracy ████████████████████  99.9%   (Epoch 60)
  Val Loss       ▓▓░░░░░░░░░░░░░░░░░░  0.0046  (Best checkpoint)
  Train Loss     ▓▓░░░░░░░░░░░░░░░░░░  0.0086

  Epoch 1   ████░░░░░░░░░░░░░░░░  70.1%  →  Val 90.4%  ✓ saved
  Epoch 4   ████████████████░░░░  97.8%  →  Val 99.1%  ✓ saved
  Epoch 7   ████████████████████  98.9%  →  Val 99.7%  ✓ saved
  Epoch 22  ████████████████████  99.8%  →  Val 99.9%  ✓ BEST
```

| Metric | Value |
|:--|:--:|
| **Best Validation Accuracy** | `99.9%` |
| **Best Validation Loss** | `0.0046` |
| **Total Training Samples** | `36,257` |
| **Total Validation Samples** | `6,399` |
| **Total Dataset** | `42,656 sequences` |
| **Classes** | `35 ISL signs` |
| **Model Architecture** | `3-layer LSTM (hidden=128)` |
| **Training Device** | `Apple MPS (M4)` |
| **Epochs Trained** | `60` |

</div>

---

<br>

## 🔮 Detection Flow

```
                        WEBCAM FRAME (30 FPS)
                               │
                               ▼
             ┌─────────────────────────────────┐
             │       OpenCV — Frame Flip       │
             │    (mirror effect for user)     │
             └────────────────┬────────────────┘
                              │
                              ▼
             ┌─────────────────────────────────┐
             │    MediaPipe — 2-Hand Track     │
             │  Up to 2 hands detected         │
             │  21 (x,y,z) landmarks per hand  │
             │  Both skeletons drawn on feed   │
             └────────────────┬────────────────┘
                              │
                              ▼
             ┌─────────────────────────────────┐
             │   Dominant Hand Selection       │
             │  (largest bounding box = front) │
             │  Wrist-normalize → 63 features  │
             └────────────────┬────────────────┘
                              │
                              ▼
             ┌─────────────────────────────────┐
             │    Sliding Window Buffer        │
             │    30 frames accumulated        │
             │    → shape (30, 63)             │
             └────────────────┬────────────────┘
                              │
                              ▼
             ┌─────────────────────────────────┐
             │    LSTM Inference (PyTorch)     │
             │    → softmax probabilities      │
             │    → top class + confidence     │
             └────────────────┬────────────────┘
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
          conf < 0.70    0.70–0.85      conf > 0.85
               │              │              ▼
          ❌ Rejected    ⚠️ Accepted     ✅ High conf
                              │              │
                              └──────┬───────┘
                                     │
                              Majority Vote (5 frames)
                                     │
                                     ▼
             ┌─────────────────────────────────┐
             │    Sentence Builder             │
             │  • Cooldown deduplication       │
             │  • Max 30 words                 │
             │  • NLP polish on demand         │
             └────────────────┬────────────────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
      🔊 gTTS Speak (EN/HI)        📋 Sentence Display
      Background thread            + Confidence Arc
      Auto-triggered               + Hindi translation
```

---

<br>

## ✨ Features

<details>
<summary><b>✋ Two-Hand Detection</b> — click to expand</summary>

<br>

MediaPipe now tracks **both hands simultaneously** — both skeletons are rendered on the camera overlay so users can see exactly what's being detected.

- Up to 2 hands tracked at 30 FPS
- Both hand skeletons drawn with full MediaPipe styling
- **Dominant hand selector** — picks the larger (closer) hand for LSTM prediction
- `num_hands` indicator shown on dashboard HUD
- No retraining required — model still receives single 63-feature vector

</details>

<details>
<summary><b>🧠 LSTM Sign Recognition</b> — click to expand</summary>

<br>

3-layer PyTorch LSTM trained from scratch on 42,000+ landmark sequences.

| Parameter | Value |
|---|---|
| Input size | 63 (21 landmarks × xyz) |
| Hidden size | 128 |
| Layers | 3 |
| Dropout | 0.3 |
| Sequence length | 30 frames |
| Output | 35 ISL classes |
| Confidence threshold | 70% |
| Vote buffer | 5 predictions |

**Supported signs:**
```
Letters:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Numbers:  One Two Three Four Five Six Seven Eight Nine
```

</details>

<details>
<summary><b>🎙️ Bilingual TTS + NLP</b> — click to expand</summary>

<br>

**Text-to-Speech:**
- Individual words spoken automatically on detection
- Full sentence spoken on demand via button or `S` key
- English and Hindi voices powered by gTTS
- Hindi TTS uses deep-translator for accurate translation
- Base64 audio returned via API — plays instantly in browser

**NLP Sentence Polishing:**
- Number words → digits (One → 1, Five → 5)
- Consecutive duplicate removal
- Auto-capitalisation of first word
- Trailing punctuation added
- Single `POST /api/nlp/polish` call

</details>

<details>
<summary><b>📖 Sign Dictionary</b> — click to expand</summary>

<br>

Slide-up reference drawer showing all 35 supported ISL signs:

- Press `D` or click Dictionary button to open
- All signs displayed as clickable cards
- Click any sign to hear it spoken aloud via TTS
- Organized alphabetically
- Works independently of camera

</details>

<details>
<summary><b>⌨️ Keyboard Shortcuts</b> — click to expand</summary>

<br>

Full keyboard accessibility built in:

| Key | Action |
|---|---|
| `Space` | Start / Stop camera |
| `C` | Clear sentence |
| `H` | Toggle Hindi voice |
| `D` | Open sign dictionary |
| `S` | Speak sentence (English) |
| `P` | Polish sentence (NLP) |
| `?` | Toggle shortcuts overlay |
| `Esc` | Close all overlays |

</details>

<details>
<summary><b>📊 Confidence Sparkline</b> — click to expand</summary>

<br>

Live Canvas chart rendered below the camera:

- Plots last 60 prediction confidence values
- Gradient fill under the line
- Colour-coded dot: 🟢 jade (>85%) / 🟠 fire (65–85%) / 🔴 rose (<65%)
- Updates every 280ms in sync with polling
- Helps users adjust hand position for optimal accuracy

</details>

<details>
<summary><b>📄 Session PDF Reports</b> — click to expand</summary>

<br>

Every session is automatically saved and downloadable as a PDF:

```
┌────────────────────────────────────────┐
│       🤙 SIGNLANG AI REPORT           │
│                                        │
│  User: Bhavya Kansal                   │
│  Date: 2026-03-14   Time: 14:32        │
│                                        │
│  Sentence: Hello how are you           │
│  Words: 4      Duration: 45s           │
│                                        │
│  WORD LOG:                             │
│  14:31:22  Hello     94.2%            │
│  14:31:28  How       88.7%            │
│  14:31:34  Are       91.3%            │
│  14:31:41  You       96.1%            │
└────────────────────────────────────────┘
```

</details>

---

<br>

## 🌐 API Routes

```
  PUBLIC ROUTES                          PRIVATE ROUTES (Auth Required)
  ─────────────                          ───────────────────────────────
  GET  /                  Landing        GET  /dashboard
  GET  /signin            Auth           GET  /history
  GET  /signup            Register       GET  /video_feed         (MJPEG stream)
  GET  /privacy           Policy         POST /api/camera/start
  GET  /terms             ToS            POST /api/camera/stop
                                         GET  /api/camera/status
                                         POST /api/sentence/clear
                                         POST /api/nlp/polish
                                         POST /api/tts/word
                                         POST /api/tts/sentence
                                         POST /api/translate/hindi
                                         POST /api/feedback
                                         GET  /api/report/latest
```

---

<br>

## 🗂️ Project Structure

```
signlang-ai/
│
├── 📄 app.py                     ← Flask application + all routes
├── 📋 requirements.txt           ← Python dependencies
├── 🐳 Dockerfile                 ← Docker config for deployment
│
├── 📂 model/
│   ├── signlang_model.pt         ← Trained 3-layer LSTM weights
│   ├── label_map.json            ← {0: "A", 1: "B", ...}
│   ├── train_lstm.py             ← Training script
│   ├── extract_landmarks.py      ← MediaPipe landmark extraction
│   ├── prepare_dataset.py        ← Dataset folder → class mapping
│   └── plots/
│       └── training_curves.png   ← Loss & accuracy plots
│
├── 📂 pipeline/
│   ├── landmark_extractor.py     ← 2-hand MediaPipe wrapper
│   ├── predictor.py              ← LSTM inference + vote buffer
│   └── sentence_builder.py      ← Word accumulator + cooldown
│
├── 📂 utils/
│   ├── tts_engine.py             ← gTTS English + Hindi TTS
│   ├── nlp_engine.py             ← Sentence polishing + translation
│   ├── report_gen.py             ← ReportLab PDF generation
│   └── sheets_client.py         ← Google Sheets session storage
│
├── 📂 static/
│   ├── logo.png                  ← Project logo (drop here)
│   ├── css/style.css             ← Full premium design system
│   └── js/
│       ├── dashboard.js          ← Camera, TTS, NLP, sparkline JS
│       └── main.js               ← Cursor, scroll reveal, animations
│
└── 📂 templates/
    ├── base.html                 ← Base layout + navbar + footer
    ├── index.html                ← Landing page
    ├── dashboard.html            ← Live detection UI
    ├── history.html              ← Session history table
    ├── signin.html               ← Auth
    ├── signup.html               ← Register
    ├── privacy.html              ← Privacy policy
    └── terms.html                ← Terms of use
```

---

<br>

## ⚙️ Setup & Run Locally

### Prerequisites

```bash
python --version   # Python 3.12+
pip --version      # pip 23+
```

### Step 1 — Clone

```bash
git clone https://github.com/BhavyaKansal20/SignLang-AI.git
cd SignLang-AI
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Prepare Dataset (only if retraining)

```bash
python model/prepare_dataset.py --src /path/to/ISL/images
python model/extract_landmarks.py --mode image --src data/raw/images
python model/train_lstm.py
```

### Step 4 — Launch

```bash
python app.py
# 🚀 Running on http://localhost:7860
```

---

<br>

## 🐳 Docker

```bash
# Build
docker build -t signlang-ai .

# Run
docker run -p 7860:7860 signlang-ai

# Open
# http://localhost:7860
```

---

<br>

## 🧰 Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|:--|:--|:--|
| **Language** | ![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white) | Core runtime |
| **Backend** | ![Flask](https://img.shields.io/badge/Flask_3.0-000000?style=flat-square&logo=flask&logoColor=white) | Web framework + MJPEG stream |
| **Deep Learning** | ![PyTorch](https://img.shields.io/badge/PyTorch_2.2-EE4C2C?style=flat-square&logo=pytorch&logoColor=white) | LSTM model training + inference |
| **Computer Vision** | ![MediaPipe](https://img.shields.io/badge/MediaPipe_0.10-0097A7?style=flat-square&logo=google&logoColor=white) | 2-hand landmark extraction |
| **Video** | ![OpenCV](https://img.shields.io/badge/OpenCV_4.9-5C3EE8?style=flat-square&logo=opencv&logoColor=white) | Webcam capture + frame processing |
| **TTS** | ![gTTS](https://img.shields.io/badge/gTTS_2.5-34A853?style=flat-square&logo=google&logoColor=white) | English + Hindi text-to-speech |
| **Translation** | ![DeepTranslator](https://img.shields.io/badge/deep--translator-1.11-FF6B35?style=flat-square) | EN → Hindi NLP translation |
| **PDF** | ![ReportLab](https://img.shields.io/badge/ReportLab_4.1-CC0000?style=flat-square) | Session PDF report generation |
| **Storage** | ![Sheets](https://img.shields.io/badge/Google_Sheets-34A853?style=flat-square&logo=google-sheets&logoColor=white) | Users + session storage |
| **Deployment** | ![HuggingFace](https://img.shields.io/badge/HuggingFace_Spaces-FFD21E?style=flat-square&logo=huggingface&logoColor=black) | Cloud hosting |
| **Container** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | Reproducible deployment |

</div>

---

<br>

## 🔐 Security Architecture

```
  USER PASSWORD
       │
       ▼
  SHA-256 Hash ──────► Stored in Google Sheets (never plain text)

  LOGIN REQUEST
       │
       ├─► Hash & Compare ──► ✅ Match → Flask Session Created
       │                      ❌ Mismatch → Redirect to signin
       │
       └─► All private routes check session["user_email"]
           Decorator: @login_req applied to every API endpoint

  CAMERA DATA
       │
       └─► Processed entirely on the server/device
           No video frames stored or transmitted
           Only recognized text saved to session history
```

---

<br>

## ⚠️ Disclaimer

> **SignLang AI is developed for educational and accessibility research purposes.**
> The model achieves 99.9% validation accuracy on the training distribution.
> Real-world accuracy may vary with lighting, camera quality and signing style.
> **Do not rely on this tool as a sole communication aid in critical situations.**

---

<br>

## 👨‍💻 Author

<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   👤  Bhavya Kansal                                          ║
║   🎓  AI Engineer | DeepTech Developer                       ║
║   🏢  Founder — MultiModex AI                                ║
║   🎓  B.Tech AI & ML — Thapar Institute of Engg. & Tech      ║
║   🔬  AI/ML Intern Trainee — IIT Ropar × NIELIT              ║
║   🌐  bhavyakansal.dev                                       ║
║   📧  kansalbhavya27@gmail.com                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

[![Portfolio](https://img.shields.io/badge/🌐%20Portfolio-bhavyakansal.dev-F0820F?style=for-the-badge&labelColor=07060A)](https://bhavyakansal.dev)
[![GitHub](https://img.shields.io/badge/GitHub-BhavyaKansal20-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/BhavyaKansal20)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kansal0920-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kansal0920)
[![MultiModex AI](https://img.shields.io/badge/🤖%20MultiModex%20AI-Platform-F0820F?style=for-the-badge&labelColor=07060A)](https://multimodexai.vercel.app)

</div>

---

<br>

## ⭐ Support

If **SignLang AI** impressed you or helped you:

```
  1. ⭐ Star this repository
  2. 🍴 Fork and build on it
  3. 📣 Share with developers and accessibility advocates
  4. 🐛 Open issues or pull requests
  5. 🤝 Help expand the sign vocabulary
```

Every star helps this project reach more people who need it. 🙏

---

<div align="center">

<br>

```
  ╔══════════════════════════════════════════════════════╗
  ║     🤙  S I G N L A N G   A I                        ║
  ║     MultiModex AI  •  © 2026 Bhavya Kansal           ║
  ╚══════════════════════════════════════════════════════╝
```

[![Live Demo](https://img.shields.io/badge/🚀%20Try%20It%20Live-SignLang%20AI%20on%20HuggingFace-F0820F?style=for-the-badge)](https://huggingface.co/spaces/BhavyaKansal20/SignLang-AI)

</div>
