"""pipeline/sentence_builder.py — Accumulates recognized words into a sentence."""

import time


class SentenceBuilder:
    """
    Collects recognized words with a cooldown to avoid duplicates.
    Provides a running sentence string.
    """

    def __init__(self, word_cooldown_sec: float = 1.5, max_words: int = 30):
        self.words            = []
        self.last_word        = ""
        self.last_word_time   = 0.0
        self.word_cooldown    = word_cooldown_sec
        self.max_words        = max_words

    def add_word(self, word: str) -> bool:
        """
        Add a word to the sentence.
        Returns True if word was added, False if rejected (duplicate / cooldown).
        """
        now = time.time()
        if (word == self.last_word and
                now - self.last_word_time < self.word_cooldown):
            return False

        self.words.append(word)
        if len(self.words) > self.max_words:
            self.words.pop(0)

        self.last_word      = word
        self.last_word_time = now
        return True

    def get_sentence(self) -> str:
        return " ".join(self.words)

    def get_words(self) -> list:
        return list(self.words)

    def reset(self):
        self.words          = []
        self.last_word      = ""
        self.last_word_time = 0.0
