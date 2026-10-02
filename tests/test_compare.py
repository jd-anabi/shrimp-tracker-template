"""Role D tests (three tools, two ages). They pass only once the functions they use exist:
load (A), motion and kinematics (B), strokes and stats (C).

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from shrimp import compare

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


def swimmer(name, v=5.0, dv=2.0, f=9.0, step=2, seconds=4.0, fps=240.0, dx=0.0, dy=0.0):
    """A shrimp swimming along x at v + dv sin(2 pi f t), tracked every `step` frames, shifted by (dx, dy)."""
    frame = np.arange(0, int(seconds * fps), step)
    t = frame / fps
    x = v * t - dv / (2 * np.pi * f) * np.cos(2 * np.pi * f * t)
    return pd.DataFrame({"track_id": name, "frame": frame, "t_s": t, "x_mm": x + dx, "y_mm": 1.0 + dy})


@pending
def test_three_tools_on_one_shrimp():
    tracks = {"tracker": swimmer("tracker"), "sam2": swimmer("sam2", dx=0.03, dy=-0.04),
              "edgetam": swimmer("edgetam", dx=-0.01)}
    table = compare.tool_comparison(tracks, window_frames=5)
    assert list(table.index) == ["tracker", "sam2", "edgetam"]
    assert table.loc["tracker", "rms_difference_mm"] == pytest.approx(0.0, abs=1e-12)
    assert table.loc["sam2", "rms_difference_mm"] == pytest.approx(0.05)  # |(0.03, -0.04)| = 0.05 mm
    assert table.loc["sam2", "bias_mm"] == pytest.approx(0.05)
    assert table.loc["edgetam", "bias_mm"] == pytest.approx(0.01)
    for tool in tracks:
        assert table.loc[tool, "mean_speed_mm_s"] == pytest.approx(5.0, rel=0.02)
        assert table.loc[tool, "stroke_hz"] == pytest.approx(9.0, abs=0.25)
        assert table.loc[tool, "stroke_period_s"] == pytest.approx(1 / table.loc[tool, "stroke_hz"])
        assert table.loc[tool, "n_frames"] == 480


@pending
def test_tool_figure_is_saved(tmp_path):
    tracks = {"tracker": swimmer("tracker"), "sam2": swimmer("sam2", dx=0.03)}
    path = compare.tool_figure(tracks, tmp_path / "figs" / "tools_A.png")
    assert Path(path).read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def per_shrimp_table(speeds, freqs):
    freqs = np.asarray(freqs, float)
    return pd.DataFrame({"shrimp": [chr(65 + i) for i in range(len(speeds))], "n_tracks": 1,
                         "duration_s": 10.0, "mean_speed_mm_s": speeds, "stroke_hz": freqs,
                         "stroke_period_s": 1 / freqs})


@pending
def test_age_comparison_uses_welch():
    young = per_shrimp_table([1.0, 2.0, 3.0], [8.0, 9.0, 10.0])
    old = per_shrimp_table([4.0, 5.0, 6.0], [8.0, 9.0, 10.0])
    table = compare.age_comparison(young, old)
    assert list(table.index) == ["mean_speed_mm_s", "stroke_hz", "stroke_period_s"]
    row = table.loc["mean_speed_mm_s"]
    assert (row["n_a"], row["n_b"]) == (3, 3)
    assert (row["mean_a"], row["mean_b"]) == (pytest.approx(2.0), pytest.approx(5.0))
    assert row["difference"] == pytest.approx(3.0)
    assert row["t"] == pytest.approx(-3.6742, abs=1e-4)  # the textbook example: df 4, p 0.0213
    assert row["p"] == pytest.approx(0.0213, abs=1e-4)
    assert table.loc["stroke_hz", "p"] == pytest.approx(1.0)  # identical frequencies


@pending
def test_age_figure_is_saved(tmp_path):
    young = per_shrimp_table([4.0, 5.0, 6.0, 5.5], [8.0, 9.0, 10.0, 9.5])
    old = per_shrimp_table([6.0, 7.0, 8.0], [7.0, 8.0, 7.5])
    path = compare.age_figure(young, old, tmp_path / "ages.png")
    assert Path(path).read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
