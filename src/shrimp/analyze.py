"""Role D: analysis. Physics from tracks.

Tests: tests/test_analyze.py. Build each function with your agent (tests first!).

Due Oct 5 (one video): speed distribution, stroke frequency, body length, Reynolds number.
Week 3 (7 videos): mean squared displacement, the Levy-flight test, everything vs age.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_speed(track: pd.DataFrame, window_frames: int = 1) -> np.ndarray:
    """Speed (mm/s) along one track, from t_s, x_mm, y_mm.

    window_frames = 1 means plain differences between consecutive frames. Larger windows
    smooth the noise (see the slides on noise and derivatives); keep the window much shorter
    than one stroke (about 240 / 9 = 27 frames at 240 fps).
    Return one value per frame (NaN where it cannot be computed).
    """
    raise NotImplementedError


def stroke_frequency_hz(signal: np.ndarray, fs_hz: float) -> float:
    """Dominant frequency (Hz) of a signal sampled at fs_hz (e.g. speed along a track).

    Remove the mean first. The frequency resolution is about 1 / (signal duration), so
    report it with the result.
    """
    raise NotImplementedError


def reynolds_number(speed_m_s: float, length_m: float, nu_m2_s: float = 1.0e-6) -> float:
    """Re = U L / nu. Default nu is roughly that of salt water near room temperature."""
    raise NotImplementedError
