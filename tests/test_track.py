"""Role C tests. Detections are built by hand, so we know which shrimp is which.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import pandas as pd
import pytest

from shrimp import track

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


def two_shrimp(n_frames=30, missing_frame=None):
    """Shrimp 1 swims right along y = 20; shrimp 2 swims up along x = 60 (1 px per frame)."""
    rows = []
    for f in range(n_frames):
        rows.append({"frame": f, "x_px": 10.0 + f, "y_px": 20.0})
        if f != missing_frame:
            rows.append({"frame": f, "x_px": 60.0, "y_px": 80.0 - f})
    df = pd.DataFrame(rows)
    df["t_s"] = df["frame"] / 240.0
    df["area_px"], df["length_px"], df["width_px"], df["angle_deg"] = 50.0, 18.0, 8.0, 0.0
    return df


def _is_one_shrimp(t):
    return t["y_px"].nunique() == 1 or t["x_px"].nunique() == 1


@pending
def test_two_shrimp_give_two_clean_tracks():
    detections = two_shrimp()
    out = track.link_detections(detections, max_step_px=5)
    assert len(out) == len(detections)
    assert out["track_id"].nunique() == 2
    assert all(_is_one_shrimp(t) for _, t in out.groupby("track_id"))


@pending
def test_short_gap_is_bridged_by_memory():
    out = track.link_detections(two_shrimp(missing_frame=12), max_step_px=5, memory_frames=2)
    assert out["track_id"].nunique() == 2


@pending
def test_without_memory_a_gap_starts_a_new_track():
    out = track.link_detections(two_shrimp(missing_frame=12), max_step_px=5, memory_frames=0)
    assert out["track_id"].nunique() == 3
    assert all(_is_one_shrimp(t) for _, t in out.groupby("track_id"))
