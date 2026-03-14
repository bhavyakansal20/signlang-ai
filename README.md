# SignLang AI 🤟

> Real-time Indian Sign Language Recognition — Text + Bilingual Voice Output

Built at **NIELIT IIT Ropar** (Jan–Jul 2026) as an AI/ML internship project.
By **Mr. Bhavya Kansal** — Founder & CEO, Multimodex AI.

---

## What it does

- Detects ISL hand gestures in real-time via your webcam
- Converts gestures → text + English/Hindi speech output
- Builds full sentences word by word
- Saves session history per user
- Generates downloadable PDF reports
- Sign in / Sign up with Google Sheets as the backend

---

## Tech Stack

| Layer | Tools |
|---|---|
| Web framework | Flask 3.0 |
| Hand tracking | MediaPipe Hands |
| Deep learning | PyTorch (3-layer LSTM) |
| Text-to-speech | gTTS (English + Hindi) |
| Translation | deep_translator |
| PDF reports | ReportLab |
| Database | Google Sheets (gspread) |
| Deployment | Hugging Face Spaces (Dockerfile) |

---

## Project Structure

```
signlang-ai/
├── app.py                        # Flask app — all routes
├── pipeline/
│   ├── landmark_extractor.py     # MediaPipe wrapper
│   ├── predictor.py              # LSTM inference + voting
│   └── sentence_builder.py      # Word accumulator
├── model/
│   ├── train_lstm.py             # Training script
│   ├── extract_landmarks.py      # Dataset → .npy landmarks
│   ├── signlang_model.pt         # Trained model (after training)
│   └── label_map.json            # Index → word mapping
├── utils/
│   ├── sheets_client.py          # Google Sheets read/write
│   ├── tts_engine.py             # gTTS English + Hindi
│   └── report_gen.py             # ReportLab PDF generator
├── templates/                    # Jinja2 HTML pages
├── static/css/style.css          # Dark glassmorphism design
├── static/js/
│   ├── main.js                   # Global animations
│   └── dashboard.js              # Camera + feedback logic
├── data/
│   ├── raw/                      # Downloaded dataset goes here
│   └── landmarks/                # Extracted .npy files
├── requirements.txt
└── Dockerfile
```

---

## Setup — Step by Step

### Step 1 — Clone and install

```bash
git clone https://github.com/BhavyaKansal20/signlang-ai
cd signlang-ai
pip install -r requirements.txt
```

### Step 2 — Google Sheets setup

#### 2a. Create a Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new blank spreadsheet
3. Name it: `SignLang AI Database`
4. Copy the **Sheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/  THIS_IS_YOUR_SHEET_ID  /edit
   ```

> The app auto-creates 3 tabs: **Users**, **Sessions**, **Feedback** on first run.

#### 2b. Create a Google Service Account

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project → name it `SignLang AI`
3. Enable **Google Sheets API** and **Google Drive API**
4. Go to **IAM & Admin → Service Accounts**
5. Create a service account → name it `signlang-sheets`
6. Click the account → **Keys** tab → **Add Key → JSON**
7. Download the JSON file → rename it `credentials.json`
8. Place it in the project root folder

#### 2c. Share the sheet with the service account

1. Open your Google Sheet
2. Click **Share**
3. Add the service account email (looks like `signlang-sheets@your-project.iam.gserviceaccount.com`)
4. Give it **Editor** access

#### 2d. Set your Sheet ID in app.py

Open `app.py` and replace:
```python
spreadsheet_id=os.environ.get("SHEET_ID", "YOUR_SHEET_ID_HERE"),
```
with your actual Sheet ID, OR set it as an environment variable:
```bash
export SHEET_ID="your_actual_sheet_id_here"
```

---

### Step 3 — Download dataset

#### Option A — Kaggle ISL (recommended for quick start)

```bash
pip install kaggle
kaggle datasets download prathumarikeri/indian-sign-language-isl
unzip indian-sign-language-isl.zip -d data/raw/images
```

#### Option B — INCLUDE-50 (IIT Bombay, word-level videos)

```bash
# Clone the dataset repo
git clone https://github.com/Sooryak12/Indian-Sign-Language-Recognition
# Copy the videos into:
# data/raw/videos/ClassName/video001.mp4 ...
```

---

### Step 4 — Extract landmarks

```bash
# For image dataset (Kaggle ISL):
python model/extract_landmarks.py --mode image --src data/raw/images

# For video dataset (INCLUDE-50):
python model/extract_landmarks.py --mode video --src data/raw/videos
```

---

### Step 5 — Train the model

```bash
python model/train_lstm.py
```

Training uses **Apple Metal (MPS)** on your MacBook M4 automatically.
After training completes:
- `model/signlang_model.pt` — saved model weights
- `model/label_map.json` — class index → word name mapping
- `model/plots/training_curves.png` — accuracy + loss plots

---

### Step 6 — Run locally

```bash
python app.py
```

Open [http://localhost:7860](http://localhost:7860)

---

## Deployment — Hugging Face Spaces

### 1. Create a new Space

- Go to [huggingface.co/new-space](https://huggingface.co/new-space)
- SDK: **Docker**
- Visibility: Public

### 2. Push your code

```bash
git init
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/signlang-ai
git add .
git commit -m "Initial commit — SignLang AI"
git push origin main
```

### 3. Set Secrets in HF Spaces

Go to your Space → **Settings → Variables and Secrets**:

| Secret Name | Value |
|---|---|
| `SHEET_ID` | Your Google Sheet ID |
| `GOOGLE_CREDENTIALS_JSON` | Paste the entire contents of your `credentials.json` file |
| `SECRET_KEY` | Any random string |

> **Note:** On HF Spaces, webcam access requires HTTPS (which HF provides by default). The MJPEG stream works correctly.

---

## Dataset Credits

- **INCLUDE-50** — IIT Bombay (Sridhar et al., 2020)
- **iSign Benchmark** — ACL 2024 (Mukherjee et al.)
- **Kaggle ISL Dataset** — Prathumarikeri

---

## License

MIT License — Free to use, modify and distribute.

---

*SignLang AI — Giving voice to every hand 🤟*
except  [error opening dir]
dataecho  [error opening dir]
# SignLang-AI  [error opening dir]

0 directories, 0 files
