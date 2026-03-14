/* SignLang AI — Dashboard v3 */
"use strict";

// ── State ──────────────────────────────────────────────────────
let isLive     = false;
let hindiOn    = false;
let rating     = 0;
let wordCount  = 0;
let pollTimer  = null;
let timerInterval = null;
let sessionStart  = null;
let lastWord   = "";
let confHistory = [];       // for sparkline
let totalWords = 0;

// ── DOM ────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const camBox    = $("camBox");
const videoFeed = $("videoFeed");
const camIdle   = $("camIdle");
const predHud   = $("predHud");
const predSign  = $("predSign");
const predHands = $("predHandsLabel");
const confArc   = $("confArc");
const confNum   = $("confNum");
const sentArea  = $("sentArea");
const wordsLog  = $("wordsLog");
const liveBadge = $("liveBadge");
const btnStart  = $("btnStart");
const btnStop   = $("btnStop");
const timerEl   = $("sessionTimer");
const sparkCvs  = $("sparkCanvas");
const sparkCtx  = sparkCvs ? sparkCvs.getContext("2d") : null;

// ── Camera ─────────────────────────────────────────────────────
async function startCamera() {
  await fetch("/api/camera/start", { method: "POST" });

  videoFeed.src = "/video_feed";
  videoFeed.classList.add("on");
  camIdle.style.display = "none";
  camBox.classList.add("live");

  btnStart.classList.add("hidden");
  btnStop.classList.remove("hidden");
  liveBadge.classList.add("on");
  timerEl.classList.add("on");

  sessionStart = Date.now();
  wordCount = 0; totalWords = 0; confHistory = [];
  sentArea.innerHTML = '<span class="sentence-ph">Listening… show your hand and start signing</span>';
  wordsLog.innerHTML = '';
  updateWordCount(0);
  updateLogCount(0);
  $("btnReport").style.display = "none";
  $("nlpOut").classList.remove("on");
  $("hindiStrip").classList.remove("on");

  isLive = true;
  timerInterval = setInterval(tickTimer, 1000);
  pollTimer     = setInterval(pollStatus, 280);
}

async function stopCamera() {
  isLive = false;
  clearInterval(pollTimer);
  clearInterval(timerInterval);

  const res  = await fetch("/api/camera/stop", { method: "POST" });
  const data = await res.json();

  videoFeed.src = "";
  videoFeed.classList.remove("on");
  camIdle.style.display = "flex";
  camBox.classList.remove("live");

  btnStop.classList.add("hidden");
  btnStart.classList.remove("hidden");
  liveBadge.classList.remove("on");
  timerEl.classList.remove("on");
  predHud.classList.remove("on");

  if (data.words && data.words.length > 0) {
    $("btnReport").style.display = "inline-flex";
  }
  toast(`Session saved — ${data.words ? data.words.length : 0} words recognized`, "ok");
}

// ── Session timer ───────────────────────────────────────────────
function tickTimer() {
  if (!sessionStart) return;
  const s = Math.floor((Date.now() - sessionStart) / 1000);
  const mm = String(Math.floor(s / 60)).padStart(2, "0");
  const ss = String(s % 60).padStart(2, "0");
  timerEl.innerHTML = `⏱ ${mm}:${ss}`;
}

// ── Status polling ──────────────────────────────────────────────
async function pollStatus() {
  try {
    const res  = await fetch("/api/camera/status");
    const data = await res.json();

    if (data.word && data.confidence > 0) {
      // Update HUD
      predSign.textContent = data.word;
      confNum.textContent  = Math.round(data.confidence) + "%";

      // Animated arc
      const pct    = data.confidence / 100;
      const circum = 2 * Math.PI * 21;
      const offset = circum - pct * circum;
      confArc.style.strokeDashoffset = offset;
      confArc.style.stroke = data.confidence > 85 ? "var(--jade)" :
                              data.confidence > 65 ? "var(--fire)" : "var(--rose)";

      // Hand count
      if (data.num_hands !== undefined && data.num_hands > 0) {
        predHands.textContent = "✋".repeat(data.num_hands) + ` ${data.num_hands}-hand`;
      } else {
        predHands.textContent = "";
      }

      predHud.classList.add("on");

      // Track confidence history for sparkline
      confHistory.push(data.confidence);
      if (confHistory.length > 60) confHistory.shift();
      drawSparkline();
    } else {
      predHud.classList.remove("on");
    }

    // Update sentence
    if (data.sentence) {
      const words = data.sentence.split(" ").filter(Boolean);
      if (words.length > 0) {
        sentArea.innerHTML = words
          .map(w => `<span class="sentence-word">${w}</span>`)
          .join(" ");
        $("sentCard").classList.add("fire-glow");
        wordCount = words.length;
        updateWordCount(wordCount);
      }
    }

    // New word → log entry
    if (data.word && data.word !== lastWord && data.confidence > 68) {
      appendLogEntry(data.word, data.confidence);
      lastWord = data.word;

      // If hindi voice on, auto-speak hindi for new word
      if (hindiOn) speakWord(data.word, "hi");
    }
  } catch (e) { /* silent */ }
}

// ── Sparkline ───────────────────────────────────────────────────
function drawSparkline() {
  if (!sparkCtx || confHistory.length < 2) return;
  const W = sparkCvs.offsetWidth;
  const H = 50;
  sparkCvs.width  = W * window.devicePixelRatio;
  sparkCvs.height = H * window.devicePixelRatio;
  sparkCtx.scale(window.devicePixelRatio, window.devicePixelRatio);

  sparkCtx.clearRect(0, 0, W, H);

  const step = W / (confHistory.length - 1);

  // Gradient fill
  const grad = sparkCtx.createLinearGradient(0, 0, 0, H);
  grad.addColorStop(0,   "rgba(240,130,15,0.25)");
  grad.addColorStop(1,   "rgba(240,130,15,0)");

  sparkCtx.beginPath();
  sparkCtx.moveTo(0, H - (confHistory[0] / 100) * H);
  for (let i = 1; i < confHistory.length; i++) {
    sparkCtx.lineTo(i * step, H - (confHistory[i] / 100) * H);
  }
  sparkCtx.lineTo(W, H);
  sparkCtx.lineTo(0, H);
  sparkCtx.closePath();
  sparkCtx.fillStyle = grad;
  sparkCtx.fill();

  // Line
  sparkCtx.beginPath();
  sparkCtx.moveTo(0, H - (confHistory[0] / 100) * H);
  for (let i = 1; i < confHistory.length; i++) {
    sparkCtx.lineTo(i * step, H - (confHistory[i] / 100) * H);
  }
  sparkCtx.strokeStyle = "var(--fire)";
  sparkCtx.lineWidth   = 2;
  sparkCtx.lineJoin    = "round";
  sparkCtx.stroke();

  // Last point dot
  const last = confHistory[confHistory.length - 1];
  sparkCtx.beginPath();
  sparkCtx.arc(W, H - (last / 100) * H, 4, 0, Math.PI * 2);
  sparkCtx.fillStyle = last > 85 ? "var(--jade)" : "var(--fire)";
  sparkCtx.fill();
}

// ── Log entries ─────────────────────────────────────────────────
function appendLogEntry(word, conf) {
  const empty = wordsLog.querySelector(".log-empty");
  if (empty) empty.remove();

  const t = new Date().toLocaleTimeString("en-IN", { hour12: false });
  const el = document.createElement("div");
  el.className = "log-item";
  el.innerHTML = `
    <span class="log-word">
      ${word}
      <span class="log-pct">${Math.round(conf)}%</span>
    </span>
    <span class="log-time">${t}</span>
  `;
  wordsLog.insertBefore(el, wordsLog.firstChild);
  totalWords++;
  updateLogCount(totalWords);
}

function updateWordCount(n) {
  $("wordCountTag").textContent = `${n} word${n !== 1 ? "s" : ""}`;
}
function updateLogCount(n) {
  $("logCount").textContent = n;
}

// ── Sentence controls ───────────────────────────────────────────
async function clearSentence() {
  await fetch("/api/sentence/clear", { method: "POST" });
  sentArea.innerHTML = '<span class="sentence-ph">Cleared — keep signing…</span>';
  wordCount = 0; updateWordCount(0);
  $("nlpOut").classList.remove("on");
  $("hindiStrip").classList.remove("on");
  $("sentCard").classList.remove("fire-glow");
  toast("Sentence cleared", "info");
}

async function polishNLP() {
  const res  = await fetch("/api/nlp/polish", { method: "POST" });
  const data = await res.json();
  if (data.polished) {
    $("nlpText").textContent = data.polished;
    $("nlpOut").classList.add("on");
    toast("Sentence polished ✨", "ok");
  } else {
    toast("Nothing to polish yet", "info");
  }
}

async function showHindiTranslation() {
  const res  = await fetch("/api/translate/hindi", { method: "POST" });
  const data = await res.json();
  if (data.hindi) {
    $("hindiText").textContent = data.hindi;
    $("hindiStrip").classList.add("on");
  } else {
    toast("Nothing to translate yet", "info");
  }
}

function copySentence() {
  const text = sentArea.textContent.trim()
    .replace("Recognized signs will build your sentence here…", "")
    .replace("Cleared — keep signing…", "")
    .replace("Listening… show your hand and start signing", "")
    .trim();
  if (!text) { toast("Nothing to copy yet", "info"); return; }
  navigator.clipboard.writeText(text).then(() => toast("Copied to clipboard!", "ok"));
}

// ── TTS ─────────────────────────────────────────────────────────
async function speakSentence(lang) {
  const res  = await fetch("/api/tts/sentence", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lang })
  });
  const data = await res.json();
  if (data.audio) {
    playAudioB64(data.audio);
    toast(`Speaking in ${lang === "hi" ? "Hindi 🇮🇳" : "English"}`, "info");
  } else {
    toast("Nothing to speak yet", "info");
  }
}

async function speakWord(word, lang = "en") {
  const res  = await fetch("/api/tts/word", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ word, lang })
  });
  const data = await res.json();
  if (data.audio) playAudioB64(data.audio);
}

function playAudioB64(b64) {
  const audio = new Audio("data:audio/mp3;base64," + b64);
  audio.play().catch(() => {});
}

// ── Hindi toggle ────────────────────────────────────────────────
function toggleHindi() {
  hindiOn = !hindiOn;
  $("hindiLabel").textContent = hindiOn ? "Hindi On" : "Hindi Off";
  $("btnHindi").style.opacity = hindiOn ? "1" : "0.7";
  toast(hindiOn ? "Hindi voice enabled 🇮🇳" : "Hindi voice off", "info");
}

// ── Dictionary ──────────────────────────────────────────────────
function openDict() {
  $("dictOverlay").classList.add("open");
  document.body.style.overflow = "hidden";
}
function closeDict(e) {
  if (!e || e.target === $("dictOverlay") || !e) {
    $("dictOverlay").classList.remove("open");
    document.body.style.overflow = "";
  }
}
function dictSpeak(sign) {
  speakWord(sign, "en");
  toast(`Speaking: ${sign}`, "info");
}

// ── Shortcuts overlay ────────────────────────────────────────────
function openShortcuts() {
  $("shortcutsOverlay").classList.add("open");
  document.body.style.overflow = "hidden";
}
function closeShortcuts(e) {
  if (!e || e.target === $("shortcutsOverlay") || !e) {
    $("shortcutsOverlay").classList.remove("open");
    document.body.style.overflow = "";
  }
}

// ── Keyboard shortcuts ───────────────────────────────────────────
document.addEventListener("keydown", e => {
  if (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT") return;
  switch (e.code) {
    case "Space":
      e.preventDefault();
      isLive ? stopCamera() : startCamera();
      break;
    case "KeyC":
      clearSentence(); break;
    case "KeyH":
      toggleHindi(); break;
    case "KeyD":
      $("dictOverlay").classList.contains("open") ? closeDict() : openDict(); break;
    case "KeyS":
      speakSentence("en"); break;
    case "KeyP":
      polishNLP(); break;
    case "Escape":
      closeDict(); closeShortcuts(); break;
    case "Slash":
      if (e.shiftKey) {
        $("shortcutsOverlay").classList.contains("open") ? closeShortcuts() : openShortcuts();
      }
      break;
  }
});

// ── Feedback ────────────────────────────────────────────────────
function setRating(v) {
  rating = v;
  document.querySelectorAll(".star").forEach(s => {
    s.classList.toggle("lit", +s.dataset.v <= v);
  });
}
async function submitFeedback() {
  if (!rating) { toast("Pick a star rating first", "err"); return; }
  const msg = $("feedMsg").value.trim();
  await fetch("/api/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rating, message: msg })
  });
  $("feedOk").classList.add("on");
  $("feedMsg").value = "";
  rating = 0;
  document.querySelectorAll(".star").forEach(s => s.classList.remove("lit"));
}

// ── PDF ─────────────────────────────────────────────────────────
function downloadReport() { window.location.href = "/api/report/latest"; }

// ── Toast ────────────────────────────────────────────────────────
function toast(msg, type = "info") {
  document.querySelectorAll(".toast").forEach(t => t.remove());
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.style.opacity = "0", 2800);
  setTimeout(() => el.remove(), 3200);
}