import os, json, time, threading, hashlib, io, base64
from datetime import datetime
from flask import (Flask, render_template, request, redirect,
                   url_for, session, Response, jsonify, send_file)
import cv2
import numpy as np

from pipeline.landmark_extractor import LandmarkExtractor
from pipeline.predictor          import GesturePredictor
from pipeline.sentence_builder   import SentenceBuilder
from utils.tts_engine            import speak, speak_hindi
from utils.nlp_engine            import polish_sentence, translate_to_hindi
from utils.sheets_client         import SheetsClient
from utils.report_gen            import generate_pdf

# ── App ───────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "signlang-ai-secret-2026")

APPS_SCRIPT_URL = os.environ.get(
    "APPS_SCRIPT_URL",
    "https://script.google.com/macros/s/AKfycbzTDIeaGWbaDrR5ivqLZ-UDMZ8lbqzX9kPi2kStNtXY_-9wncQawQq7EV4FdkamHTud/exec"
)
sheets     = SheetsClient(apps_script_url=APPS_SCRIPT_URL)
extractor  = None   # lazy-loaded on first frame
predictor  = GesturePredictor(model_path="model/signlang_model.pt",
                               label_map_path="model/label_map.json")
sentence_b = SentenceBuilder()

# ── Global state ──────────────────────────────────────────────
camera_lock   = threading.Lock()
current_frame = None
current_pred  = {"word": "", "confidence": 0.0, "sentence": "", "num_hands": 0}
camera_active = False
cap           = None
session_words = []
session_start = None

# ✅ Server-side per-user landmark buffers (keyed by email)
# Avoids Flask cookie 4KB limit which silently dropped buffer data
user_buffers = {}

# ── Helpers ───────────────────────────────────────────────────
def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()

def login_req(f):
    from functools import wraps
    @wraps(f)
    def dec(*a, **kw):
        if "user_email" not in session:
            return redirect(url_for("signin"))
        return f(*a, **kw)
    return dec

# ── Routes ────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html",
        logged_in="user_email" in session,
        user_name=session.get("user_name", ""))

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if "user_email" in session: return redirect(url_for("dashboard"))
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        pw    = request.form.get("password", "")
        user  = sheets.verify_user(email, hash_pw(pw))
        if user:
            session["user_email"] = email
            session["user_name"]  = user.get("name", "User")
            return redirect(url_for("dashboard"))
        error = "Invalid email or password."
    return render_template("signin.html", error=error)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_email" in session: return redirect(url_for("dashboard"))
    error = None
    if request.method == "POST":
        name  = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        pw    = request.form.get("password", "")
        if len(pw) < 6:
            error = "Password must be at least 6 characters."
        elif sheets.email_exists(email):
            error = "An account with this email already exists."
        else:
            sheets.add_user({"name": name, "email": email,
                "password_hash": hash_pw(pw),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            session["user_email"] = email
            session["user_name"]  = name
            return redirect(url_for("dashboard"))
    return render_template("signup.html", error=error)

@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_req
def dashboard():
    try:
        with open("model/label_map.json") as f:
            lm = json.load(f)
        signs = sorted(lm.values())
    except Exception:
        signs = []
    return render_template("dashboard.html",
        user_name=session.get("user_name", "User"),
        signs=signs)

@app.route("/history")
@login_req
def history():
    user_sessions = sheets.get_sessions(session["user_email"])
    return render_template("history.html",
        user_name=session.get("user_name", "User"),
        sessions=user_sessions)

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

# ── Camera API ────────────────────────────────────────────────

@app.route("/api/camera/start", methods=["POST"])
@login_req
def start_camera():
    global session_words, session_start, current_pred
    email = session["user_email"]
    session_words      = []
    session_start      = time.time()
    user_buffers[email] = []   # ✅ clear server-side buffer for this user
    current_pred       = {"word": "", "confidence": 0.0, "sentence": "", "num_hands": 0}
    sentence_b.reset()
    print(f"[Start] Session started for {email}")
    return jsonify({"status": "started"})

@app.route("/api/frame", methods=["POST"])
@login_req
def process_frame():
    global current_pred, session_words, extractor

    # Lazy-load MediaPipe on first frame
    if extractor is None:
        extractor = LandmarkExtractor()

    data = request.get_json()
    if not data or "frame" not in data:
        return jsonify(current_pred)

    # Decode base64 JPEG from browser
    try:
        img_data  = data["frame"].split(",")[1]
        img_bytes = base64.b64decode(img_data)
        np_arr    = np.frombuffer(img_bytes, np.uint8)
        frame     = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"[Frame] Decode error: {e}")
        return jsonify(current_pred)

    if frame is None:
        return jsonify(current_pred)

    # Extract landmarks — no cv2.flip (browser already mirrors front cam)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    lm, annotated, num_hands = extractor.extract(rgb, frame.copy())

    email = session["user_email"]

    # Ensure buffer exists for this user
    if email not in user_buffers:
        user_buffers[email] = []

    if lm is not None:
        # ✅ Server-side buffer — no cookie size limit
        user_buffers[email].append(lm.tolist())
        if len(user_buffers[email]) > 30:
            user_buffers[email].pop(0)

        buf_len = len(user_buffers[email])
        print(f"[Frame] hands={num_hands} lm=True buf={buf_len}")

        if buf_len == 30:
            word, conf = predictor.predict(np.array(user_buffers[email]))
            print(f"[Frame] prediction: word={word} conf={conf:.2f}")

            if conf > 0.70 and word:
                added = sentence_b.add_word(word)
                if added:
                    session_words.append({
                        "word":       word,
                        "confidence": round(conf * 100, 1),
                        "timestamp":  datetime.now().strftime("%H:%M:%S")
                    })
                current_pred = {
                    "word":       word,
                    "confidence": round(conf * 100, 1),
                    "sentence":   sentence_b.get_sentence(),
                    "num_hands":  num_hands,
                }
            else:
                current_pred = {
                    "word":       "",
                    "confidence": round(conf * 100, 1),
                    "sentence":   sentence_b.get_sentence(),
                    "num_hands":  num_hands,
                }
    else:
        print(f"[Frame] hands=0 lm=False buf={len(user_buffers[email])}")

    return jsonify(current_pred)

@app.route("/api/camera/stop", methods=["POST"])
@login_req
def stop_camera():
    global session_words, session_start
    email    = session["user_email"]
    duration = int(time.time() - (session_start or time.time()))

    # Clear server-side buffer for this user
    user_buffers[email] = []

    if session_words:
        sheets.add_session({
            "email":      email,
            "name":       session.get("user_name", ""),
            "date":       datetime.now().strftime("%Y-%m-%d"),
            "time":       datetime.now().strftime("%H:%M:%S"),
            "words":      ", ".join([w["word"] for w in session_words]),
            "word_count": str(len(session_words)),
            "sentence":   sentence_b.get_sentence(),
            "duration":   str(duration),
        })

    result = {"status": "stopped", "words": session_words,
              "sentence": sentence_b.get_sentence(), "duration": duration}
    session_words = []
    print(f"[Stop] Session ended for {email} — {len(result['words'])} words")
    return jsonify(result)

@app.route("/api/camera/status")
@login_req
def camera_status():
    return jsonify(current_pred)

@app.route("/api/sentence/clear", methods=["POST"])
@login_req
def clear_sentence():
    sentence_b.reset()
    return jsonify({"status": "cleared"})

@app.route("/video_feed")
@login_req
def video_feed():
    def gen():
        while True:
            with camera_lock:
                frame = current_frame
            if frame is None:
                time.sleep(0.05)
                continue
            ret, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if not ret: continue
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                   + buf.tobytes() + b"\r\n")
            time.sleep(0.03)
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

# ── NLP / TTS API ─────────────────────────────────────────────

@app.route("/api/nlp/polish", methods=["POST"])
@login_req
def nlp_polish():
    words    = sentence_b.get_words()
    polished = polish_sentence(words)
    return jsonify({"polished": polished})

@app.route("/api/tts/word", methods=["POST"])
@login_req
def tts_word():
    data = request.get_json()
    word = data.get("word", "")
    lang = data.get("lang", "en")
    if not word:
        return jsonify({"error": "no word"}), 400
    path = speak(word, lang=lang)
    if not path or not os.path.exists(path):
        return jsonify({"error": "tts failed"}), 500
    with open(path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()
    return jsonify({"audio": audio_b64, "word": word, "lang": lang})

@app.route("/api/tts/sentence", methods=["POST"])
@login_req
def tts_sentence():
    data  = request.get_json()
    lang  = data.get("lang", "en")
    words = sentence_b.get_words()
    text  = polish_sentence(words)
    if not text:
        return jsonify({"error": "empty sentence"}), 400
    if lang == "hi":
        text = translate_to_hindi(text)
    path = speak(text, lang=lang)
    if not path or not os.path.exists(path):
        return jsonify({"error": "tts failed"}), 500
    with open(path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()
    return jsonify({"audio": audio_b64, "text": text, "lang": lang})

@app.route("/api/translate/hindi", methods=["POST"])
@login_req
def translate_hindi():
    words    = sentence_b.get_words()
    polished = polish_sentence(words)
    hindi    = translate_to_hindi(polished) if polished else ""
    return jsonify({"hindi": hindi, "original": polished})

# ── Feedback ──────────────────────────────────────────────────

@app.route("/api/feedback", methods=["POST"])
@login_req
def feedback():
    d = request.get_json()
    sheets.add_feedback({
        "email":     session["user_email"],
        "name":      session.get("user_name", ""),
        "rating":    str(d.get("rating", "")),
        "message":   d.get("message", ""),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    return jsonify({"status": "ok"})

# ── PDF ───────────────────────────────────────────────────────

@app.route("/api/report/latest")
@login_req
def latest_pdf():
    sessions = sheets.get_sessions(session["user_email"])
    if not sessions:
        return jsonify({"error": "No sessions"}), 404
    latest = sessions[-1]
    path   = generate_pdf(session.get("user_name", "User"),
                          session["user_email"], latest)
    return send_file(path, as_attachment=True,
                     download_name="SignLang_AI_Report.pdf",
                     mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7860, threaded=True)
