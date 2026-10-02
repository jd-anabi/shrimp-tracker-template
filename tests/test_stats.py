"""Role C tests (one value per shrimp, mean and SD, Welch's test). Every value can be checked by hand.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import numpy as np
import pandas as pd
import pytest

from shrimp import stats

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


def summary_table():
    """What strokes.summarize_tracks returns: pieces A.1, A.2 and A2 are one shrimp; C3 is shrimp C."""
    return pd.DataFrame({
        "track_id": ["A.1", "A.2", "A2", "B", "C3"],
        "n_frames": [480, 240, 240, 960, 480],
        "duration_s": [2.0, 1.0, 1.0, 4.0, 2.0],
        "mean_speed_mm_s": [4.0, 6.0, 5.0, 3.0, 7.0],
        "stroke_hz": [8.0, 10.0, 9.0, 8.5, 10.0],
        "stroke_resolution_hz": [0.5, 1.0, 1.0, 0.25, 0.5],
    })


@pending
def test_pieces_of_one_shrimp_are_combined():
    s = stats.per_shrimp(summary_table()).set_index("shrimp")
    assert list(s.index) == ["A", "B", "C"]
    assert s.loc["A", "n_tracks"] == 3
    assert s.loc["A", "duration_s"] == pytest.approx(4.0)
    assert s.loc["A", "mean_speed_mm_s"] == pytest.approx((2 * 4 + 1 * 6 + 1 * 5) / 4)  # weighted by duration
    assert s.loc["A", "stroke_hz"] == pytest.approx((2 * 8 + 1 * 10 + 1 * 9) / 4)
    assert s.loc["A", "stroke_period_s"] == pytest.approx(4 / 35)
    assert s.loc["C", "mean_speed_mm_s"] == pytest.approx(7.0)


@pending
def test_describe():
    d = stats.describe([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0, np.nan])
    assert d["n"] == 8
    assert d["mean"] == pytest.approx(5.0)
    assert d["sd"] == pytest.approx(np.sqrt(32 / 7))  # sum of squared deviations is 32, n - 1 = 7
    assert d["sem"] == pytest.approx(np.sqrt(32 / 7) / np.sqrt(8))


@pending
def test_welch_textbook_example():
    # means 2 and 5, both SDs 1, n = 3 each: t = -3 / sqrt(1/3 + 1/3) = -3.674, df = 4, p = 0.0213
    r = stats.welch_test([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
    assert r["t"] == pytest.approx(-3.6742, abs=1e-4)
    assert r["df"] == pytest.approx(4.0)
    assert r["p"] == pytest.approx(0.0213, abs=1e-4)
    assert r["difference"] == pytest.approx(3.0)


@pending
def test_welch_unequal_variances_and_nan():
    # a: mean 4, variance 4, n 3;  b: mean 25, variance 500/3, n 4 (the NaN is ignored)
    # se^2 = 4/3 + (500/3)/4 = 43,  t = (4 - 25)/sqrt(43) = -3.2025
    # df = 43^2 / ((4/3)^2/2 + (125/3)^2/3) = 3.190
    r = stats.welch_test([2.0, 4.0, 6.0, np.nan], [10.0, 20.0, 30.0, 40.0])
    assert r["t"] == pytest.approx(-21 / np.sqrt(43))
    assert r["df"] == pytest.approx(43 ** 2 / ((4 / 3) ** 2 / 2 + (125 / 3) ** 2 / 3))
    assert r["p"] == pytest.approx(0.0452, abs=5e-4)  # t table, 3.19 degrees of freedom
    assert r["difference"] == pytest.approx(21.0)
