"""Role D tests (analysis). Expected values come from physics you can do by hand.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import numpy as np
import pandas as pd
import pytest

from shrimp import analyze

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


def straight_track(vx_mm_s=3.0, vy_mm_s=4.0, n=50, fs=240.0):
    t = np.arange(n) / fs
    return pd.DataFrame({"t_s": t, "x_mm": vx_mm_s * t, "y_mm": vy_mm_s * t})


@pending
def test_constant_velocity_gives_constant_speed():
    v = analyze.compute_speed(straight_track(), window_frames=1)  # |(3, 4)| = 5 mm/s
    assert len(v) == 50
    assert np.all(np.isnan(v) | np.isclose(v, 5.0))
    assert np.sum(~np.isnan(v)) >= 45


@pending
def test_smoothing_does_not_change_a_constant_speed():
    v = analyze.compute_speed(straight_track(), window_frames=9)
    assert np.all(np.isnan(v) | np.isclose(v, 5.0))


@pending
def test_stroke_frequency_of_a_9_hz_oscillation():
    fs = 240.0
    t = np.arange(int(3 * fs)) / fs  # 3 s, so the resolution is about 1/3 Hz
    speed = 5.0 + 3.0 * np.sin(2 * np.pi * 9.0 * t)
    assert analyze.stroke_frequency_hz(speed, fs) == pytest.approx(9.0, abs=1 / 3)


@pending
def test_stroke_frequency_survives_noise():
    fs = 240.0
    t = np.arange(int(3 * fs)) / fs
    rng = np.random.default_rng(0)
    speed = 5.0 + 3.0 * np.sin(2 * np.pi * 9.0 * t) + rng.normal(0, 1.5, t.size)
    assert analyze.stroke_frequency_hz(speed, fs) == pytest.approx(9.0, abs=1 / 3)


@pending
def test_reynolds_number():
    # U = 5 mm/s, L = 0.5 mm, nu = 1e-6 m^2/s  ->  Re = 2.5
    assert analyze.reynolds_number(5e-3, 5e-4) == pytest.approx(2.5)
    assert analyze.reynolds_number(5e-3, 5e-4, nu_m2_s=0.5e-6) == pytest.approx(5.0)
