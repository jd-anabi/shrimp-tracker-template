"""Role C tests (strokes and Reynolds number). Expected values come from physics you can do by hand.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
The summarize_tracks test also needs kinematics.compute_speed (Role B).
"""

import numpy as np
import pandas as pd
import pytest

from shrimp import strokes

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


@pending
def test_stroke_frequency_of_a_9_hz_oscillation():
    fs = 240.0
    t = np.arange(int(3 * fs)) / fs  # 3 s, so the resolution is about 1/3 Hz
    speed = 5.0 + 3.0 * np.sin(2 * np.pi * 9.0 * t)
    assert strokes.stroke_frequency_hz(speed, fs) == pytest.approx(9.0, abs=1 / 3)


@pending
def test_stroke_frequency_survives_noise():
    fs = 240.0
    t = np.arange(int(3 * fs)) / fs
    rng = np.random.default_rng(0)
    speed = 5.0 + 3.0 * np.sin(2 * np.pi * 9.0 * t) + rng.normal(0, 1.5, t.size)
    assert strokes.stroke_frequency_hz(speed, fs) == pytest.approx(9.0, abs=1 / 3)


@pending
def test_stroke_frequency_ignores_nan_at_the_ends():
    fs = 240.0
    t = np.arange(int(3 * fs)) / fs
    speed = 5.0 + 3.0 * np.sin(2 * np.pi * 9.0 * t)
    speed[:4] = np.nan  # what a smoothing window leaves at the ends of a track
    speed[-4:] = np.nan
    assert strokes.stroke_frequency_hz(speed, fs) == pytest.approx(9.0, abs=1 / 3)


def swimmer(track_id, n_rows, v=5.0, dv=2.0, f=9.0, step=1, fps=240.0):
    """A shrimp swimming along x at v + dv sin(2 pi f t) mm/s, marked every `step` frames."""
    frame = np.arange(n_rows) * step
    t = frame / fps
    x = v * t - dv / (2 * np.pi * f) * np.cos(2 * np.pi * f * t)
    return pd.DataFrame({"track_id": track_id, "frame": frame, "t_s": t, "x_mm": x, "y_mm": 1.0})


@pending
def test_summary_has_one_row_per_long_enough_track():
    # B was marked every 2nd frame (Clip Settings step size 2): 120 samples per second
    tracks = pd.concat([swimmer("A", 480), swimmer("B", 720, v=3.0, step=2), swimmer("C", 100)])
    s = strokes.summarize_tracks(tracks, window_frames=9, min_duration_s=1.0).set_index("track_id")
    assert sorted(s.index) == ["A", "B"], "the 100-frame (0.4 s) track is too short"
    assert s.loc["A", "mean_speed_mm_s"] == pytest.approx(5.0, rel=0.02)
    assert s.loc["B", "mean_speed_mm_s"] == pytest.approx(3.0, rel=0.02)
    assert s.loc["A", "stroke_hz"] == pytest.approx(9.0, abs=0.5)
    assert s.loc["B", "stroke_hz"] == pytest.approx(9.0, abs=0.2), "the sampling rate must come from t_s"
    assert s.loc["A", "duration_s"] == pytest.approx(2.0, abs=0.01)
    assert s.loc["B", "duration_s"] == pytest.approx(6.0, abs=0.01)
    assert s.loc["A", "stroke_resolution_hz"] == pytest.approx(0.5, abs=0.01)


@pending
def test_reynolds_number():
    # U = 5 mm/s, L = 0.5 mm, nu = 1e-6 m^2/s  ->  Re = 2.5
    assert strokes.reynolds_number(5e-3, 5e-4) == pytest.approx(2.5)
    assert strokes.reynolds_number(5e-3, 5e-4, nu_m2_s=0.5e-6) == pytest.approx(5.0)
