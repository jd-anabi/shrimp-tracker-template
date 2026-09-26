"""Role C: tracking. Links detections in consecutive frames into tracks (one per shrimp).

Tests: tests/test_track.py. Build each function with your agent (tests first!).
You may use trackpy (`uv add trackpy`) or write the linking yourself, but either way
you must show on the synthetic video that it works.

At 240 fps a shrimp moves about a pixel per frame, far less than the distance between
shrimp, so linking is easy. The hard cases are collisions (two blobs merge) and
shrimp at the dish wall. When in doubt, end the track and start a new one.
"""

from __future__ import annotations

import pandas as pd


def link_detections(detections: pd.DataFrame, max_step_px: float,
                    memory_frames: int = 0) -> pd.DataFrame:
    """Return the detections with an integer track_id column added.

    max_step_px: largest distance a shrimp can move between consecutive frames.
    memory_frames: how many frames a shrimp may go undetected and still keep its track_id.
    """
    raise NotImplementedError
