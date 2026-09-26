"""Role D tests (validation scores). The tracks are built by hand, so the right scores are known.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import numpy as np
import pandas as pd
import pytest

from shrimp import validate

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


def truth_table():
    """Two shrimp, 10 frames, 40 px apart."""
    rows = [{"frame": f, "t_s": f / 240, "track_id": k, "x_px": 10.0 + f, "y_px": 20.0 + 40 * k}
            for f in range(10) for k in (0, 1)]
    return pd.DataFrame(rows)


@pending
def test_perfect_tracks_score_perfectly():
    tracks = truth_table().assign(track_id=lambda d: d["track_id"] + 7)  # ids need not match
    s = validate.compare_to_truth(tracks, truth_table(), max_dist_px=2.0)
    assert s["recall"] == pytest.approx(1.0) and s["precision"] == pytest.approx(1.0)
    assert s["rms_error_px"] == pytest.approx(0.0, abs=1e-9)
    assert s["id_switches"] == 0


@pending
def test_offset_and_identity_swap_are_measured():
    tracks = truth_table()
    tracks["x_px"] += 0.3
    tracks["y_px"] += 0.4  # every position is off by 0.5 px
    late = tracks["frame"] >= 5
    tracks.loc[late, "track_id"] = 1 - tracks.loc[late, "track_id"]  # the two ids swap at frame 5
    s = validate.compare_to_truth(tracks, truth_table(), max_dist_px=2.0)
    assert s["rms_error_px"] == pytest.approx(0.5)
    assert s["id_switches"] == 2


@pending
def test_missed_detections_lower_recall_only():
    tracks = truth_table().drop(index=np.arange(0, 20, 4))  # drop 5 of the 20 positions
    s = validate.compare_to_truth(tracks, truth_table(), max_dist_px=2.0)
    assert s["recall"] == pytest.approx(0.75)
    assert s["precision"] == pytest.approx(1.0)
