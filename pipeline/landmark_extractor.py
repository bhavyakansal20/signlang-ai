"""pipeline/landmark_extractor.py — MediaPipe Hands wrapper (two-hand support)."""

import numpy as np
import mediapipe as mp
import cv2


class LandmarkExtractor:
    """
    Uses MediaPipe Hands to extract 21 3D landmarks from each frame.
    Supports up to 2 hands — draws BOTH on the overlay for visual accuracy,
    but returns a normalized 63-element vector from the DOMINANT hand only
    (model was trained on single-hand 63-feature sequences).

    Two-hand signs:  both hands are tracked and displayed.
    One-hand signs:  only one hand skeleton appears, prediction unchanged.
    """

    def __init__(self, max_hands: int = 2, min_detection_conf: float = 0.6,
                 min_tracking_conf: float = 0.5):
        self.mp_hands   = mp.solutions.hands
        self.mp_draw    = mp.solutions.drawing_utils
        self.mp_styles  = mp.solutions.drawing_styles
        self.hands      = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,           # detect up to 2 hands
            min_detection_confidence=min_detection_conf,
            min_tracking_confidence=min_tracking_conf,
        )

    @staticmethod
    def _normalize(hand_lm) -> np.ndarray:
        """Extract + normalise 21 landmarks → flat (63,) vector."""
        raw = np.array([[lm.x, lm.y, lm.z] for lm in hand_lm.landmark],
                       dtype=np.float32)
        raw -= raw[0]
        scale = np.max(np.abs(raw)) + 1e-9
        raw  /= scale
        return raw.flatten()

    @staticmethod
    def _hand_size(hand_lm) -> float:
        """Bounding box diagonal — used to pick dominant (larger/closer) hand."""
        xs = [lm.x for lm in hand_lm.landmark]
        ys = [lm.y for lm in hand_lm.landmark]
        return ((max(xs) - min(xs)) ** 2 + (max(ys) - min(ys)) ** 2) ** 0.5

    def extract(self, rgb_frame: np.ndarray, annotated_frame: np.ndarray):
        """
        Process one frame.
        Returns:
            landmarks  (np.ndarray shape [63]) from dominant hand, or None
            annotated  (np.ndarray) — frame with skeletons for ALL detected hands
            num_hands  (int) — 0, 1 or 2
        """
        results = self.hands.process(rgb_frame)

        if not results.multi_hand_landmarks:
            return None, annotated_frame, 0

        num_hands = len(results.multi_hand_landmarks)

        # Draw ALL detected hands on the overlay
        for hand_lm in results.multi_hand_landmarks:
            self.mp_draw.draw_landmarks(
                annotated_frame,
                hand_lm,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_styles.get_default_hand_landmarks_style(),
                self.mp_styles.get_default_hand_connections_style(),
            )

        # Pick dominant hand for prediction (larger = closer/more prominent)
        if num_hands == 1:
            dominant_lm = results.multi_hand_landmarks[0]
        else:
            dominant_lm = max(results.multi_hand_landmarks,
                              key=lambda lm: self._hand_size(lm))

        return self._normalize(dominant_lm), annotated_frame, num_hands