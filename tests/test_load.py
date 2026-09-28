"""Role A tests (import and calibration). Every expected value can be checked by hand.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import numpy as np
import pytest
from conftest import straight_track, tracker_text

from shrimp import load
from shrimp.formats import TRACK_COLUMNS

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


@pending
def test_fps_from_two_stopwatch_readings():
    # the stopwatch reads 1.00 s at frame 100 and 3.00 s at frame 580: 480 frames in 2 s
    assert load.fps_from_stopwatch(100, 1.00, 580, 3.00) == pytest.approx(240.0)


@pending
def test_fps_rejects_equal_times():
    with pytest.raises(ValueError):
        load.fps_from_stopwatch(100, 2.0, 200, 2.0)


@pending
def test_manifest_needs_a_slow_motion_fps_true(tmp_path):
    good = tmp_path / "good.csv"
    good.write_text("video_file,fps_true\nday1.MOV,239.6\n")
    assert load.load_manifest(good)["fps_true"].iloc[0] == pytest.approx(239.6)
    for i, bad_row in enumerate(["day1.MOV,", "day1.MOV,30.0"]):  # empty; a re-timed 30 fps copy
        bad = tmp_path / f"bad{i}.csv"
        bad.write_text("video_file,fps_true\n" + bad_row + "\n")
        with pytest.raises(ValueError):
            load.load_manifest(bad)


@pending
def test_read_a_file_exported_by_tracker(tracker_file):
    path = tracker_file("A.csv", ",mass A,,,\n"
                                 "t,frame,x,y,\n"
                                 "0.000000E0,1.200000E2,1.500000E0,-2.000000E0,\n"
                                 "4.166667E-3,1.210000E2,1.520000E0,-2.010000E0,\n"
                                 "8.333333E-3,1.220000E2,,,\n"      # frame 122 was not marked
                                 "1.250000E-2,1.230000E2,1.560000E0,-2.030000E0,\n")
    t = load.read_tracker_csv(path)
    assert list(t["frame"]) == [120, 121, 123]
    assert np.issubdtype(t["frame"].dtype, np.integer)
    assert list(t["x"]) == pytest.approx([1.5, 1.52, 1.56])
    assert list(t["y"]) == pytest.approx([-2.0, -2.01, -2.03])
    assert list(t["t"]) == pytest.approx([0.0, 1 / 240, 3 / 240], rel=1e-5)


@pending
def test_read_tabs_without_name_line_and_extra_columns(tracker_file):
    # copied from Tracker's table instead of exported: no name line, tabs, formatted numbers
    path = tracker_file("B.txt", "t\tframe\tx\ty\tv\n0.000\t10\t3.000\t4.000\t\n0.004\t11\t3.010\t4.000\t2.40\n")
    t = load.read_tracker_csv(path)
    assert list(t["frame"]) == [10, 11]
    assert list(t["x"]) == pytest.approx([3.0, 3.01])


@pending
def test_read_needs_the_frame_column(tracker_file):
    path = tracker_file("C.csv", ",mass C,,\nt,x,y,\n0.000000E0,1.000000E0,1.000000E0,\n")
    with pytest.raises(ValueError):
        load.read_tracker_csv(path)


@pending
def test_read_refuses_several_point_masses_in_one_file(tracker_file):
    path = tracker_file("AB.csv", "#multi:\n,mass A,,,mass B,,,\nt,frame,x,y,frame,x,y,\n"
                                  "0.000000E0,0.000000E0,1.000000E0,1.000000E0,0.000000E0,5.000000E0,5.000000E0,\n")
    with pytest.raises(ValueError):
        load.read_tracker_csv(path)


@pending
def test_one_track_per_file_and_time_from_fps_true(tracker_file):
    fps_true = 239.5  # measured with the stopwatch and typed into Tracker's Clip Settings
    tracker_file("A.csv", tracker_text(straight_track("A", start_frame=120, fps=fps_true), fps_tracker=fps_true))
    path = tracker_file("B.txt", tracker_text(straight_track("B", y0=3.0, fps=fps_true), fps_tracker=fps_true,
                                              name="mass B", sep="\t"))
    tracker_file("still.csv", tracker_text(straight_track("S", vx_mm_s=0, vy_mm_s=0), fps_tracker=fps_true),
                 folder="tracks/extra")  # files in subfolders are not tracks
    tracks = load.load_tracks(path.parent, fps_true)
    assert set(TRACK_COLUMNS) <= set(tracks.columns)
    assert sorted(tracks["track_id"].unique()) == ["A", "B"]
    assert len(tracks) == 2 * 240
    assert np.allclose(tracks["t_s"], tracks["frame"] / fps_true)
    a = tracks[tracks["track_id"] == "A"]
    assert a["frame"].iloc[0] == 120 and a["t_s"].iloc[0] == pytest.approx(120 / fps_true)


@pending
def test_wrong_frame_rate_in_tracker_is_caught(tracker_file):
    # Clip Settings were left at 30 fps (a re-timed copy): Tracker's time step is 8x too long
    path = tracker_file("A.csv", tracker_text(straight_track("A"), fps_tracker=30.0))
    with pytest.raises(ValueError):
        load.load_tracks(path.parent, 240.0)


@pending
def test_positions_not_in_mm_are_caught(tracker_file):
    in_pixels = straight_track("A").assign(x_mm=lambda d: d["x_mm"] * 47.0, y_mm=lambda d: d["y_mm"] * 47.0)
    path = tracker_file("A.csv", tracker_text(in_pixels), folder="pixels")  # no calibration stick
    with pytest.raises(ValueError):
        load.load_tracks(path.parent, 240.0)
    in_metres = straight_track("A").assign(x_mm=lambda d: d["x_mm"] / 1000, y_mm=lambda d: d["y_mm"] / 1000)
    path = tracker_file("A.csv", tracker_text(in_metres), folder="metres")  # stick length typed as 0.02
    with pytest.raises(ValueError):
        load.load_tracks(path.parent, 240.0)


@pending
def test_empty_folder(tmp_path):
    with pytest.raises(FileNotFoundError):
        load.load_tracks(tmp_path, 240.0)
