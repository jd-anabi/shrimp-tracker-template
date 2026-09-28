"""Role C: strokes and Reynolds number. What each shrimp's swimming looks like.

Tests: tests/test_strokes.py. Build each function with your agent (tests first!).
summarize_tracks uses kinematics.compute_speed (Role B): write it once that is merged.

Per track or per frame? summarize_tracks gives one value per track (one shrimp's stretch of
swimming). For a per-frame distribution, use kinematics.per_frame_speeds instead. Say which
one you report: they answer different questions.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def stroke_frequency_hz(signal: np.ndarray, fs_hz: float) -> float:
    """Dominant frequency (Hz) of a signal sampled at fs_hz (e.g. the speed along one track).

    Ignore NaN values at the ends. Remove the mean first. The frequency resolution is about
    1 / (signal duration), so report it with the result.
    """
    raise NotImplementedError


def summarize_tracks(tracks: pd.DataFrame, window_frames: int = 9, min_duration_s: float = 1.0) -> pd.DataFrame:
    """One row per track lasting at least min_duration_s (t_s of the last row minus the first);
    shorter tracks are dropped.

    Columns: track_id, n_frames, duration_s, mean_speed_mm_s (kinematics.compute_speed with
    window_frames, NaN ignored), stroke_hz and stroke_resolution_hz (stroke_frequency_hz of that
    speed, and 1 / duration_s). The sampling rate comes from t_s (1 / median time step), not
    from the video file.
    """
    raise NotImplementedError


def reynolds_number(speed_m_s: float, length_m: float, nu_m2_s: float = 1.0e-6) -> float:
    """Re = U L / nu. Default nu is roughly that of salt water near room temperature."""
    raise NotImplementedError
