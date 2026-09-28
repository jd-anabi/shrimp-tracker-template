"""Role D tests (report). They pass only once every role's functions are written:
analyze_video uses load (A), kinematics (B) and strokes (C).

The example data in data/example/ were made with known physics (see data/example/README.md),
so the expected values below are that known physics, not the output of anybody's code.
Until everything is written these tests show as "xfailed". When they pass, delete the
@pending line above them.
"""

from pathlib import Path

import numpy as np
import pytest
from conftest import straight_track, tracker_text

from shrimp import report

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")

EXAMPLE = Path(__file__).resolve().parents[1] / "data" / "example"


@pending
def test_example_data_gives_the_known_physics():
    r = report.analyze_video(EXAMPLE, 240.0)
    assert r["n_files"] == 7
    assert r["n_tracks"] == 8, "B has a jump (B.1 and B.2); C and C2 are two tracks"
    assert r["track_speed_mean_mm_s"] == pytest.approx(4.875, rel=0.02)
    assert r["stroke_hz_mean"] == pytest.approx(9.0625, abs=0.15)
    assert r["noise_mm"] == pytest.approx(0.006, rel=0.15)
    assert len(r["summary"]) == 8
    # 17,215 tracked rows in those 8 tracks, minus the w - 1 = 8 rows per track where the 9-frame window does not fit
    assert len(r["frame_speeds_mm_s"]) == 17215 - 8 * 8


def two_straight_tracks(tracker_file):
    tracker_file("A.csv", tracker_text(straight_track("A", n_frames=480)))
    path = tracker_file("B.csv", tracker_text(straight_track("B", n_frames=480, y0=3.0), name="mass B"))
    return path.parent


@pending
def test_without_a_still_object_the_noise_is_nan(tracker_file):
    r = report.analyze_video(two_straight_tracks(tracker_file), 240.0)
    assert r["n_files"] == 2 and r["n_tracks"] == 2
    assert r["track_speed_mean_mm_s"] == pytest.approx(5.0)
    assert r["frame_speed_mean_mm_s"] == pytest.approx(5.0)
    assert np.isnan(r["noise_mm"])


@pending
def test_figures_are_saved(tracker_file, tmp_path):
    r = report.analyze_video(two_straight_tracks(tracker_file), 240.0)
    paths = report.make_figures(r, tmp_path / "figures", prefix="test_")
    names = {Path(p).name for p in paths}
    assert {"test_speed_histogram.png", "test_tracks.png"} <= names
    for p in paths:
        assert Path(p).read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", f"{p} is not a PNG file"
