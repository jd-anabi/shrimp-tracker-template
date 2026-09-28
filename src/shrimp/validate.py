"""Role D (validation): how good is the tracking?

Tests: tests/test_validate.py. Build it with your agent (tests first!).
Track one shrimp twice for about 200 frames (the autotracker, and a teammate marking every
frame by hand): the difference between the two measures your tracking error.
"""

from __future__ import annotations

import pandas as pd


def compare_tracks(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    """Compare two trackings of the SAME shrimp (TRACK_COLUMNS tables), in the frames both contain.

    Returns a dict with at least:
        n_frames            number of frames in both tracks
        rms_difference_mm   root-mean-square distance between the two positions
        max_difference_mm   largest distance (a big value means one tracking jumped)
        bias_mm             length of the mean difference vector (the two methods marking
                            different points of the body, e.g. head vs. center)
    Raise ValueError if the tracks have no frame in common.
    """
    raise NotImplementedError
