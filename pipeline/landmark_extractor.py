"""pipeline/landmark_extractor.py — MediaPipe Hands wrapper (two-hand support)."""
import numpy as np
import cv2

class LandmarkExtractor:
    def __init__(self, max_hands=2, min_detection_conf=0.6, min_tracking_conf=0.5):
        import mediapipe as mp
        self.mp_hands  = mp.solutions.hands
        self.mp_draw   = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        self.hands     = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_conf,
            min_tracking_confidence=min_tracking_conf,
        )

    @staticmethod
    def _normalize(hand_lm):
        raw = np.array([[lm.x, lm.y, lm.z] for lm in hand_lm.landmark], dtype=np.float32)
        raw -= raw[0]
        scale = np.max(np.abs(raw)) + 1e-9
        raw  /= scale
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
        for hand_lm in results.multi_hand_landmarks:
            self.mp_draw.draw_landmarks(
                annotated_frame, hand_lm,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_styles.get_default_hand_landmarks_style(),
                self.mp_styles.get_default_hand_connections_style(),
            )
        dominant_lm = max(results.multi_hand_landmarks, key=lambda lm: self._hand_size(lm)) if num_hands > 1 else results.multi_hand_landmarks[0]
        return self._normalize(dominant_lm), annotated_frame, num_hands
