"""
Image-quality diagnostics (Section 2.2 / Phase 3 of the CUE proposal).

Flags frames that are too blurry or too dark/bright to trust downstream
detection results on.
"""

import cv2
import numpy as np
from dataclasses import dataclass


@dataclass
class FrameQuality:
    blur_score: float
    brightness: float
    is_usable: bool
    reason: str


def compute_blur_score(gray_frame: np.ndarray) -> float:
    """
    Variance of the Laplacian - a common, cheap sharpness proxy.
    Lower values mean a blurrier image.
    """
    return cv2.Laplacian(gray_frame, cv2.CV_64F).var()


def compute_brightness(gray_frame: np.ndarray) -> float:
    """Mean pixel intensity, 0-255."""
    return float(np.mean(gray_frame))


def assess_frame(frame: np.ndarray, blur_threshold: float = 100.0,
                  min_brightness: float = 40.0, max_brightness: float = 220.0) -> FrameQuality:
    """
    Run both checks and decide whether this frame is trustworthy enough
    to feed into detection. Thresholds are starting points - tune them
    against your own camera and lighting once you have real footage.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur_score = compute_blur_score(gray)
    brightness = compute_brightness(gray)

    if blur_score < blur_threshold:
        return FrameQuality(blur_score, brightness, False, "too blurry")
    if brightness < min_brightness:
        return FrameQuality(blur_score, brightness, False, "too dark")
    if brightness > max_brightness:
        return FrameQuality(blur_score, brightness, False, "overexposed")

    return FrameQuality(blur_score, brightness, True, "ok")
