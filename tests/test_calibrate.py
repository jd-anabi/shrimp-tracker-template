"""Role A tests. The expected values come from arithmetic you can check by hand.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import pandas as pd
import pytest

from shrimp import calibrate

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


@pending
def test_fps_from_two_stopwatch_readings():
    # stopwatch reads 1.00 s at frame 100 and 3.00 s at frame 580: 480 frames in 2 s
    assert calibrate.fps_from_stopwatch(100, 1.00, 580, 3.00) == pytest.approx(240.0)


@pending
def test_fps_rejects_equal_times():
    with pytest.raises(ValueError):
        calibrate.fps_from_stopwatch(100, 2.0, 200, 2.0)


@pending
def test_scale_from_horizontal_ruler():
    # 10 mm between marks 300 px apart: 1000 * 10 / 300 um per px
    assert calibrate.scale_from_ruler((10, 20), (310, 20), 10.0) == pytest.approx(1000 * 10 / 300)


@pending
def test_scale_from_diagonal_ruler():
    # 3-4-5 triangle: the points are 500 px apart, 20 mm apart -> 40 um per px
    assert calibrate.scale_from_ruler((0, 0), (300, 400), 20.0) == pytest.approx(40.0)


@pending
def test_add_physical_units():
    table = pd.DataFrame({"frame": [0, 240, 480], "x_px": [0.0, 100.0, 250.0], "y_px": [50.0, 50.0, 0.0]})
    out = calibrate.add_physical_units(table, fps_true=240.0, um_per_px=32.0)
    assert list(out["t_s"]) == pytest.approx([0.0, 1.0, 2.0])
    assert list(out["x_mm"]) == pytest.approx([0.0, 3.2, 8.0])
    assert list(out["y_mm"]) == pytest.approx([1.6, 1.6, 0.0])
    assert "t_s" not in table.columns, "the input table must not be modified"


@pending
def test_manifest_needs_fps_and_scale(tmp_path):
    good = tmp_path / "good.csv"
    good.write_text("video_file,fps_true,um_per_px\nday1.MOV,240.1,32.5\n")
    assert calibrate.load_manifest(good)["fps_true"].iloc[0] == pytest.approx(240.1)
    bad = tmp_path / "bad.csv"
    bad.write_text("video_file,um_per_px\nday1.MOV,32.5\n")
    with pytest.raises(ValueError):
        calibrate.load_manifest(bad)
