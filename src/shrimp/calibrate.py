"""Role A: video & calibration. Turns frames and pixels into seconds and millimetres.

Tests: tests/test_calibrate.py. Build each function with your agent (tests first!).
"""

from __future__ import annotations

import pandas as pd


def fps_from_stopwatch(frame_a: int, time_a_s: float, frame_b: int, time_b_s: float) -> float:
    """True frame rate from two frames of the stopwatch clip.

    Look at the stopwatch clip, note two frames far apart and the stopwatch reading in
    each (seconds). fps_true = (frame_b - frame_a) / (time_b_s - time_a_s).
    The farther apart the two frames, the smaller the relative error.
    Raise ValueError if the two times are equal.
    """
    raise NotImplementedError


def scale_from_ruler(point_a_px: tuple[float, float], point_b_px: tuple[float, float],
                     distance_mm: float) -> float:
    """Micrometres per pixel from two points (x_px, y_px) on the ruler clip `distance_mm` apart.

    Use points as far apart as possible (e.g. 0 mm and 30 mm marks).
    Returns um_per_px = 1000 * distance_mm / (pixel distance between the points).
    """
    raise NotImplementedError


def add_physical_units(table: pd.DataFrame, fps_true: float, um_per_px: float) -> pd.DataFrame:
    """Return a copy of `table` with t_s = frame / fps_true, x_mm and y_mm filled in.

    x_mm = x_px * um_per_px / 1000 (same for y). Axes stay as in the image (y points down).
    """
    raise NotImplementedError


def load_manifest(path: str = "data/manifest.csv") -> pd.DataFrame:
    """Read data/manifest.csv and check the required columns are present and filled."""
    raise NotImplementedError
