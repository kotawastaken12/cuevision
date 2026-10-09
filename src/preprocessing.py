"""
Local preprocessing primitives (Section 2.2 of the CUE proposal):
CLAHE contrast correction and edge-preserving smoothing.
"""

import cv2
import numpy as np


def apply_clahe(frame: np.ndarray, clip_limit: float = 2.0, tile_grid_size=(8, 8)) -> np.ndarray:
    """
    Apply Contrast Limited Adaptive Histogram Equalization on the
    luminance channel only, so colors don't get distorted.
    """
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    l_channel = clahe.apply(l_channel)

    merged = cv2.merge((l_channel, a_channel, b_channel))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def apply_bilateral(frame: np.ndarray, d: int = 9, sigma_color: float = 75, sigma_space: float = 75) -> np.ndarray:
    """Edge-preserving smoothing - reduces sensor noise without blurring boundaries."""
    return cv2.bilateralFilter(frame, d, sigma_color, sigma_space)


def apply_gaussian(frame: np.ndarray, kernel_size=(5, 5), sigma: float = 0) -> np.ndarray:
    """Simple Gaussian blur - cheaper than bilateral, use when speed matters more than edge fidelity."""
    return cv2.GaussianBlur(frame, kernel_size, sigma)
