"""pipeline/landmark_extractor.py"""
import os
import numpy as np
import cv2

os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"

class LandmarkExtractor:
    def __init__(self, max_hands=2, min_detection_conf=0.6, min_tracking_conf=0.5):
        import mediapipe as mp
        self.mp      = mp
        self.hands   = mp.solutions.hands.Hands(
            static_image_mode=True,    # ← changed from False
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_conf,
            min_tracking_confidence=min_tracking_conf,
            model_complexity=0,        # ← added: lighter + faster on CPU
        )
        self.draw    = mp.solutions.drawing_utils
        self.styles  = mp.solutions.drawing_styles
        self.CONN    = mp.solutions.hands.HAND_CONNECTIONS

    @staticmethod
    def _normalize(hand_lm):
        raw = np.array([[lm.x, lm.y, lm.z] for lm in hand_lm.landmark], dtype=np.float32)
        raw -= raw[0]
        raw /= (np.max(np.abs(raw)) + 1e-9)
        return raw.flatten()

    @staticmethod
    def _hand_size(hand_lm):
        xs = [lm.x for lm in hand_lm.landmark]
        ys = [lm.y for lm in hand_lm.landmark]
        return ((max(xs)-min(xs))**2 + (max(ys)-min(ys))**2)**0.5

    def extract(self, rgb_frame, annotated_frame):
        results = self.hands.process(rgb_frame)
        if not results.multi_hand_landmarks:
            return None, annotated_frame, 0
        num_hands = len(results.multi_hand_landmarks)
        for h in results.multi_hand_landmarks:
            self.draw.draw_landmarks(annotated_frame, h, self.CONN,
                self.styles.get_default_hand_landmarks_style(),
                self.styles.get_default_hand_connections_style())
        dominant = max(results.multi_hand_landmarks, key=self._hand_size) if num_hands > 1 else results.multi_hand_landmarks[0]
        return self._normalize(dominant), annotated_frame, num_hands
