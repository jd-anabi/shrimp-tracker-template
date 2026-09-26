"""Role B: detection. Finds every shrimp in every frame.

Tests: tests/test_detect.py. Build each function with your agent (tests first!).

Idea: shrimp move, the dish, cysts and scratches do not. The per-pixel median of many
frames spread over the video is an image of the empty scene (the background).
Shrimp are the pixels that differ from it.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def estimate_background(path, n_samples: int = 100) -> np.ndarray:
    """Per-pixel median of `n_samples` frames spread evenly over the video (2-D uint8).

    Read frames with shrimp.video (never load the whole video). A shrimp that stays still
    for most of the video will end up in the background: say so in your results.
    """
    raise NotImplementedError


def detect_shrimp(frame: np.ndarray, background: np.ndarray,
                  min_area_px: float, max_area_px: float) -> pd.DataFrame:
    """Detect shrimp in one grayscale frame.

    Returns one row per shrimp with the columns in shrimp.formats.DETECTION_COLUMNS
    (frame and t_s may be left as NaN here; detect_video fills them in).
    Centroids must be sub-pixel. Blobs outside [min_area_px, max_area_px] are rejected;
    choose these limits from the calibration (um_per_px), not by trial and error.
    """
    raise NotImplementedError


def detect_video(path, background: np.ndarray, fps_true: float,
                 min_area_px: float, max_area_px: float) -> pd.DataFrame:
    """Run detect_shrimp on every frame (streaming) and fill in frame and t_s."""
    raise NotImplementedError
