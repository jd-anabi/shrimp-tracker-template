"""Role D tests (validation). Every expected value can be checked by hand.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import numpy as np
import pytest
from conftest import straight_track

from shrimp import validate

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


@pending
def test_a_constant_offset():
    a = straight_track(n_frames=240)
    b = a.assign(x_mm=a["x_mm"] + 0.003, y_mm=a["y_mm"] + 0.004)  # 0.005 mm away in every frame
    s = validate.compare_tracks(a, b)
    assert s["n_frames"] == 240
    assert s["rms_difference_mm"] == pytest.approx(0.005)
    assert s["max_difference_mm"] == pytest.approx(0.005)
    assert s["bias_mm"] == pytest.approx(0.005)


@pending
def test_only_frames_in_both_count():
    a = straight_track(n_frames=240)                   # frames 0-239
    b = straight_track(n_frames=200, start_frame=100)  # frames 100-299, a different line
    b = b.drop(index=[10, 11]).reset_index(drop=True)  # frames 110 and 111 not marked
    s = validate.compare_tracks(a, b)
    assert s["n_frames"] == 140 - 2
    both = a[a["frame"].isin(b["frame"])].set_index("frame")
    d = np.hypot(both["x_mm"] - b.set_index("frame").loc[both.index, "x_mm"],
                 both["y_mm"] - b.set_index("frame").loc[both.index, "y_mm"])
    assert s["rms_difference_mm"] == pytest.approx(np.sqrt(np.mean(d ** 2)))


@pending
def test_one_bad_frame_shows_in_the_max():
    a = straight_track(n_frames=100)
    b = a.copy()
    b.loc[50, "x_mm"] += 1.0
    s = validate.compare_tracks(a, b)
    assert s["max_difference_mm"] == pytest.approx(1.0)
    assert s["rms_difference_mm"] == pytest.approx(np.sqrt(1.0 / 100))


@pending
def test_no_common_frame():
    with pytest.raises(ValueError):
        validate.compare_tracks(straight_track(n_frames=10), straight_track(n_frames=10, start_frame=50))
