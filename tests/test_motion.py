"""Role B tests (velocity and acceleration). Expected values come from physics you can do by hand.

Until the function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import numpy as np
import pandas as pd
import pytest

from shrimp import motion

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


def track_from(x, y, frames, fps=240.0):
    frames = np.asarray(frames)
    return pd.DataFrame({"track_id": "A", "frame": frames, "t_s": frames / fps, "x_mm": x, "y_mm": y})


@pending
def test_constant_acceleration_is_exact():
    # x = 1 + 2 t + (1/2)(30) t^2,  y = -1 - 3 t + (1/2)(-12) t^2: v and a are known at every time
    frames = np.arange(0, 400, 2)  # every 2nd frame, as tracked with Tracker's step size 2
    t = frames / 240.0
    out = motion.velocity_acceleration(track_from(1 + 2 * t + 15 * t ** 2, -1 - 3 * t - 6 * t ** 2, frames))
    inner = out.iloc[2:-2]
    assert np.allclose(inner["vx_mm_s"], 2 + 30 * inner["t_s"])
    assert np.allclose(inner["vy_mm_s"], -3 - 12 * inner["t_s"])
    assert np.allclose(inner["ax_mm_s2"], 30.0)
    assert np.allclose(inner["ay_mm_s2"], -12.0)
    assert np.allclose(inner["speed_mm_s"], np.hypot(inner["vx_mm_s"], inner["vy_mm_s"]))


@pending
def test_ends_are_nan_and_rows_are_kept():
    frames = np.arange(50)
    out = motion.velocity_acceleration(track_from(0.1 * frames, 0 * frames, frames))
    assert len(out) == 50 and list(out["frame"]) == list(frames)
    assert np.isnan(out["vx_mm_s"].iloc[0]) and np.isnan(out["vx_mm_s"].iloc[-1])
    assert np.isnan(out["ax_mm_s2"].iloc[:2]).all() and np.isnan(out["ax_mm_s2"].iloc[-2:]).all()
    assert np.isfinite(out["vx_mm_s"].iloc[1:-1]).all() and np.isfinite(out["ax_mm_s2"].iloc[2:-2]).all()


@pending
def test_uniform_circular_motion():
    # speed V = 5 mm/s on a circle of radius 2 mm: |a| = V^2 / R = 12.5 mm/s^2 toward the center
    fps, V, R = 120.0, 5.0, 2.0
    frames = np.arange(300)
    t = frames / fps
    th = V / R * t
    out = motion.velocity_acceleration(track_from(R * np.cos(th), R * np.sin(th), frames, fps)).iloc[2:-2]
    assert np.allclose(out["speed_mm_s"], V, rtol=1e-3)
    assert np.allclose(np.hypot(out["ax_mm_s2"], out["ay_mm_s2"]), V ** 2 / R, rtol=2e-3)


@pending
def test_a_skipped_frame_is_not_a_neighbour():
    frames = np.delete(np.arange(0, 60, 2), 15)  # frame 30 was not tracked
    t = frames / 240.0
    out = motion.velocity_acceleration(track_from(5.0 * t, 0 * t, frames)).set_index("frame")
    good = out["vx_mm_s"].dropna()
    assert np.allclose(good, 5.0), "a gap must not fake a change of speed"
    assert np.isnan(out.loc[28, "vx_mm_s"]) and np.isnan(out.loc[32, "vx_mm_s"])
    assert np.isnan(out.loc[[26, 28, 32, 34], "ax_mm_s2"]).all()
    assert np.allclose(out["ax_mm_s2"].dropna(), 0.0, atol=1e-9)


@pending
def test_noise_follows_trackers_formulas():
    # independent position noise sigma: sigma_v = sigma / (sqrt(2) dt), sigma_a = sqrt(14) sigma / (7 dt^2)
    rng = np.random.default_rng(3)
    sigma, n, step = 0.006, 20000, 2
    frames = np.arange(n) * step
    dt = step / 240.0
    out = motion.velocity_acceleration(track_from(rng.normal(0, sigma, n), rng.normal(0, sigma, n), frames))
    assert np.nanstd(out["vx_mm_s"]) == pytest.approx(sigma / (np.sqrt(2) * dt), rel=0.05)
    assert np.nanstd(out["ay_mm_s2"]) == pytest.approx(np.sqrt(14) * sigma / (7 * dt ** 2), rel=0.05)
