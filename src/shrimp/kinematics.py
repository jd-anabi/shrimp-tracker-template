"""Role B: kinematics. Speeds from positions, smoothing, tracking noise, and impossible jumps.

Tests: tests/test_kinematics.py. Build each function with your agent (tests first!).
Every function takes tracks in the format of shrimp.formats.TRACK_COLUMNS (positions in mm,
time t_s in s). Use t_s for time: never assume a fixed frame rate or that no frame is missing.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_speed(track: pd.DataFrame, window_frames: int = 2) -> np.ndarray:
    """Speed (mm/s) along ONE track (rows in time order), from t_s, x_mm, y_mm.

    window_frames = w is the number of rows the difference spans: the displacement over
    (w - 1) steps divided by the time between them (slide 29). w = 2 means consecutive rows;
    an odd w >= 3 is centered on the row. Use t_s for the time, so a missing frame does not
    fake a speed-up. Keep w much shorter than one stroke (about 240 / 9 = 27 frames).
    Return one value per row (NaN where the window does not fit).
    """
    raise NotImplementedError


def per_frame_speeds(tracks: pd.DataFrame, window_frames: int = 9) -> np.ndarray:
    """Speeds of every track (compute_speed on each track_id separately), pooled together
    with NaN removed: the per-frame speed distribution."""
    raise NotImplementedError


def position_noise_mm(still: pd.DataFrame) -> float:
    """Tracking noise sigma (mm) from a track of something that does not move (a cyst stuck to
    the dish): the standard deviation of x_mm and of y_mm about their means, averaged over x and y."""
    raise NotImplementedError


def find_jumps(track: pd.DataFrame, max_speed_mm_s: float = 100.0) -> np.ndarray:
    """Frame numbers at which the step from the previous row of ONE track implies a speed above
    max_speed_mm_s (use t_s for the time between them). A shrimp cannot do that: it is the
    autotracker jumping to something else (slide 24)."""
    raise NotImplementedError


def split_at_jumps(tracks: pd.DataFrame, max_speed_mm_s: float = 100.0, min_frames: int = 24) -> pd.DataFrame:
    """Cut every track at each of its jumps and keep the pieces with at least min_frames rows.

    A track without jumps keeps its name. A track with jumps becomes <track_id>.1,
    <track_id>.2, ... in time order (numbered after the short pieces are dropped). A few bad
    frames between two jumps become a short piece and are dropped.
    """
    raise NotImplementedError
