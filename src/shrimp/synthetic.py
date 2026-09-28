"""Role D (validation): fake tracks whose physics we know exactly.

Tests: tests/test_synthetic.py. Build each function with your agent (tests first!).

If your analysis cannot recover the speed and stroke frequency of a track you made yourself,
it cannot be trusted on real shrimp.
"""

from __future__ import annotations

import pandas as pd


def make_synthetic_track(duration_s: float = 10.0, fps: float = 240.0, speed_mm_s: float = 5.0,
                         stroke_hz: float = 9.0, surge: float = 0.6, noise_mm: float = 0.006,
                         turn_sd_rad: float = 0.02, radius_mm: float = 15.0, x0_mm: float = 0.0,
                         y0_mm: float = 0.0, start_frame: int = 0, seed: int = 0,
                         track_id: str = "S") -> pd.DataFrame:
    """A fake shrimp with known physics, as a table with shrimp.formats.TRACK_COLUMNS.

    It starts at (x0_mm, y0_mm) and swims along a slowly turning heading (a random turn of
    standard deviation turn_sd_rad every frame) at speed_mm_s * (1 + surge * sin(2 pi stroke_hz t)),
    so its mean speed is speed_mm_s and its speed oscillates at stroke_hz. Whenever the next
    position would be more than radius_mm from the center, it turns around instead.
    Independent noise of standard deviation noise_mm is added to x and to y in every frame
    (after the path is made). There are round(duration_s * fps) rows: frame = start_frame,
    start_frame + 1, ...; t_s = frame / fps. The same seed gives the same track.
    """
    raise NotImplementedError


def write_tracker_csv(track: pd.DataFrame, path, name: str = "mass A") -> None:
    """Write one track the way Tracker exports it (see the top of load.py): a first line with
    the name, then the column names t, frame, x, y, then one row per frame, comma separated,
    numbers with at least 7 significant digits (t_s as t, x_mm as x, y_mm as y)."""
    raise NotImplementedError
