"""Role D (validation): how good are our tracks?

Tests: tests/test_validate.py. Build it with your agent (tests first!).
Use it twice: on the synthetic video (truth = generator output) and on your real video
(truth = ~200 frames of a few shrimp tracked by hand).
"""

from __future__ import annotations

import pandas as pd


def compare_to_truth(tracks: pd.DataFrame, truth: pd.DataFrame, max_dist_px: float) -> dict:
    """Match tracked positions to true positions frame by frame and score them.

    Returns a dict with at least:
        recall        fraction of true positions with a tracked position within max_dist_px
        precision     fraction of tracked positions with a true position within max_dist_px
        rms_error_px  root-mean-square distance of matched pairs
        id_switches   number of times a true shrimp's matched track_id changes
    """
    raise NotImplementedError
