"""utils/tts_engine.py — gTTS wrapper for English + Hindi output."""

import os
import tempfile
from gtts import gTTS
from deep_translator import GoogleTranslator


def speak(text: str, lang: str = "en"):
    """
    Convert text to speech and save as temp MP3.
    Returns the file path so Flask can serve it.
    lang: "en" for English, "hi" for Hindi
    """
    try:
        tts  = gTTS(text=text, lang=lang, slow=False)
        path = os.path.join(tempfile.gettempdir(), f"signlang_{lang}_{abs(hash(text))}.mp3")
        tts.save(path)
        return path
    except Exception as e:
        print(f"[TTS Error] {e}")
        return None


def translate_to_hindi(text: str) -> str:
    """Translate English word/sentence to Hindi using deep_translator."""
    try:
        return GoogleTranslator(source="en", target="hi").translate(text)
    except Exception:
        return text


def speak_hindi(text: str):
    """Translate to Hindi and speak."""
    hindi_text = translate_to_hindi(text)
    return speak(hindi_text, lang="hi")
