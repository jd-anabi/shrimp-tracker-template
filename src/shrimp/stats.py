"""Role C: one value per shrimp, mean and SD, and the significance of a difference between ages.

Tests: tests/test_stats.py. Build each function with your agent (tests first!).

The sample is SHRIMP, not frames: each shrimp contributes one average speed, one frequency and one
period. Frames of the same shrimp are not independent measurements, so using them as samples makes
any difference look significant.
"""

from __future__ import annotations

import pandas as pd


def per_shrimp(summary: pd.DataFrame) -> pd.DataFrame:
    """One row per shrimp from a strokes.summarize_tracks table.

    Pieces of the same shrimp are combined: the shrimp is the letters at the start of track_id, so A,
    A2, A.1 and A2.3 are all shrimp A (a track_id without leading letters is its own shrimp).
    Columns: shrimp, n_tracks, duration_s (sum over pieces), mean_speed_mm_s and stroke_hz (means of
    the pieces weighted by their duration_s), stroke_period_s = 1 / stroke_hz. Sorted by shrimp.
    """
    raise NotImplementedError


def describe(values) -> dict:
    """{"n", "mean", "sd", "sem"} of the finite values: sd with n - 1 in the denominator,
    sem = sd / sqrt(n)."""
    raise NotImplementedError


def welch_test(a, b) -> dict:
    """Welch's two-sample t-test (unequal variances), two-sided, on the finite values of a and b.

    Returns {"t", "df", "p", "difference"} with difference = mean(b) - mean(a),
    t = (mean(a) - mean(b)) / sqrt(s_a^2 / n_a + s_b^2 / n_b) and df from the Welch-Satterthwaite
    formula. scipy is installed (scipy.stats.ttest_ind with equal_var=False).
    """
    raise NotImplementedError
