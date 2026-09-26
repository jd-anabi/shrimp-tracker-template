"""Role D (validation): synthetic videos where the true tracks are known.

Tests: tests/test_synthetic.py. Build it with your agent (tests first!).

If your tracker cannot recover tracks you drew yourself, it cannot be trusted on real
shrimp. Make the fake shrimp realistic: dark elongated blobs of the right size, moving at
a few mm/s with a stroke-like speed oscillation (~9 Hz), plus noise and a static "cyst".
"""

from __future__ import annotations

import pandas as pd


def make_synthetic_video(path, n_shrimp: int = 5, n_frames: int = 480, fps: float = 240.0,
                         width_px: int = 640, height_px: int = 480, um_per_px: float = 32.0,
                         speed_mm_s: float = 5.0, stroke_hz: float = 9.0,
                         body_length_um: float = 500.0, noise_sd: float = 3.0,
                         seed: int = 0) -> pd.DataFrame:
    """Write a video file to `path` and return the ground truth.

    The returned DataFrame has the columns in shrimp.formats.TRUTH_COLUMNS
    (frame, t_s, track_id, x_px, y_px): one row per shrimp per frame, using the same
    image axes as the tracker (x right, y down). Use `seed` so results are reproducible.
    """
    raise NotImplementedError
