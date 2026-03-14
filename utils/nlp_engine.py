"""utils/nlp_engine.py — NLP helpers: sentence polishing + translation."""

import re
from deep_translator import GoogleTranslator


# ── Sentence polisher ──────────────────────────────────────────
# Simple rule-based approach (no heavy NLP deps needed at runtime)
_FILLER = {"A", "AN", "THE"}   # common words that often get doubled


def polish_sentence(words: list) -> str:
    """
    Given a list of recognized sign words, return a readable sentence:
    - Capitalise first word
    - Convert number words to digits
    - Remove back-to-back identical words
    - Add a period at the end
    """
    if not words:
        return ""

    _NUM_MAP = {
        "ONE": "1", "TWO": "2", "THREE": "3", "FOUR": "4", "FIVE": "5",
        "SIX": "6", "SEVEN": "7", "EIGHT": "8", "NINE": "9",
    }

    cleaned = []
    prev = None
    for w in words:
        upper = w.upper()
        # Replace number words
        w_out = _NUM_MAP.get(upper, w)
        # Deduplicate consecutive identical tokens
        if w_out.upper() == (prev or "").upper():
            continue
        cleaned.append(w_out)
        prev = w_out

    if not cleaned:
        return ""

    sentence = " ".join(cleaned)
    # Capitalise
    sentence = sentence[0].upper() + sentence[1:]
    # Add trailing period if missing
    if sentence[-1] not in ".!?":
        sentence += "."
    return sentence


# ── Translator ─────────────────────────────────────────────────
def translate_to_hindi(text: str) -> str:
    try:
        return GoogleTranslator(source="en", target="hi").translate(text)
    except Exception:
        return text


def translate_to_gujarati(text: str) -> str:
    try:
        return GoogleTranslator(source="en", target="gu").translate(text)
    except Exception:
        return text