"""Role D tests (synthetic tracks). Expected values come from the physics you put in.

These tests do not use the other roles' code, so they can pass before anything else is written.
Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import numpy as np
import pandas as pd
import pytest

from shrimp import synthetic
from shrimp.formats import TRACK_COLUMNS

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


def speeds(track):
    """Frame-to-frame speed (mm/s), computed here so this test does not depend on Role B."""
    return np.hypot(np.diff(track["x_mm"]), np.diff(track["y_mm"])) / np.diff(track["t_s"])


@pending
def test_table_format():
    t = synthetic.make_synthetic_track(duration_s=2.0, fps=240.0, start_frame=100, track_id="Q")
    assert list(t.columns[:5]) == TRACK_COLUMNS
    assert len(t) == 480
    assert list(t["frame"]) == list(range(100, 580))
    assert np.allclose(t["t_s"], t["frame"] / 240.0)
    assert set(t["track_id"]) == {"Q"}


@pending
def test_known_mean_speed_and_stroke_frequency():
    fs = 240.0
    t = synthetic.make_synthetic_track(duration_s=10.0, fps=fs, speed_mm_s=5.0, stroke_hz=9.0, noise_mm=0.0)
    v = speeds(t)
    assert v.mean() == pytest.approx(5.0, rel=0.01)
    spectrum = np.abs(np.fft.rfft(v - v.mean()))
    freqs = np.fft.rfftfreq(v.size, d=1 / fs)
    assert freqs[np.argmax(spectrum)] == pytest.approx(9.0, abs=0.2)


@pending
def test_starts_where_asked_and_stays_in_the_dish():
    t = synthetic.make_synthetic_track(duration_s=60.0, noise_mm=0.0, x0_mm=3.0, y0_mm=-4.0, seed=3)
    assert (t["x_mm"].iloc[0], t["y_mm"].iloc[0]) == pytest.approx((3.0, -4.0))
    assert np.hypot(t["x_mm"], t["y_mm"]).max() <= 15.0 + 1e-9


@pending
def test_noise_is_what_was_asked():
    # a shrimp that does not swim is a still object: what remains is the added noise
    t = synthetic.make_synthetic_track(duration_s=10.0, speed_mm_s=0.0, noise_mm=0.01)
    assert t["x_mm"].std() == pytest.approx(0.01, rel=0.05)
    assert t["y_mm"].std() == pytest.approx(0.01, rel=0.05)


@pending
def test_same_seed_same_track():
    a = synthetic.make_synthetic_track(seed=5)
    b = synthetic.make_synthetic_track(seed=5)
    c = synthetic.make_synthetic_track(seed=6)
    pd.testing.assert_frame_equal(a, b)
    assert not np.allclose(a["x_mm"], c["x_mm"])


@pending
def test_written_like_tracker(tmp_path):
    t = synthetic.make_synthetic_track(duration_s=0.5, start_frame=120)
    path = tmp_path / "A.csv"
    synthetic.write_tracker_csv(t, path, name="mass A")
    lines = path.read_text().splitlines()
    assert "mass A" in lines[0]
    assert [c for c in lines[1].split(",") if c] == ["t", "frame", "x", "y"]
    back = pd.read_csv(path, skiprows=1)
    assert np.allclose(back["frame"], t["frame"])
    assert np.allclose(back["x"], t["x_mm"], rtol=1e-6, atol=1e-9)
    assert np.allclose(back["y"], t["y_mm"], rtol=1e-6, atol=1e-9)
