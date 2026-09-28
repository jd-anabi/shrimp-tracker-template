"""Role B tests (kinematics). Expected values come from physics you can do by hand.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import numpy as np
import pandas as pd
import pytest
from conftest import straight_track

from shrimp import kinematics

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


@pending
def test_constant_velocity_gives_constant_speed():
    v = kinematics.compute_speed(straight_track(n_frames=50), window_frames=2)  # |(3, 4)| = 5 mm/s
    assert len(v) == 50
    assert np.all(np.isnan(v) | np.isclose(v, 5.0))
    assert np.sum(~np.isnan(v)) >= 45


@pending
def test_smoothing_does_not_change_a_constant_speed():
    v = kinematics.compute_speed(straight_track(n_frames=50), window_frames=9)
    assert np.all(np.isnan(v) | np.isclose(v, 5.0))
    assert np.sum(~np.isnan(v)) >= 40


@pending
def test_a_missing_frame_does_not_fake_a_speed_up():
    t = straight_track(n_frames=50).drop(index=20).reset_index(drop=True)  # frame 20 was not marked
    v = kinematics.compute_speed(t, window_frames=2)
    assert np.all(np.isnan(v) | np.isclose(v, 5.0))


@pending
def test_speed_noise_follows_the_smoothing_formula():
    # slide 29: constant 5 mm/s along x, plus independent position noise sigma in x and y in every frame
    fs, sigma, n = 240.0, 0.002, 20000
    rng = np.random.default_rng(1)
    t = np.arange(n) / fs
    noisy = pd.DataFrame({"t_s": t, "x_mm": 5.0 * t + rng.normal(0, sigma, n), "y_mm": rng.normal(0, sigma, n)})
    for w in (2, 9):
        v = kinematics.compute_speed(noisy, window_frames=w)
        expected = np.sqrt(2) * sigma / ((w - 1) / fs)  # sigma_v(w) = sqrt(2) sigma / ((w - 1) dt)
        assert np.nanstd(v) == pytest.approx(expected, rel=0.06), f"window_frames={w}"


@pending
def test_per_frame_speeds_pool_every_track():
    tracks = pd.concat([straight_track("A", n_frames=100, vx_mm_s=3.0, vy_mm_s=0.0),
                        straight_track("B", n_frames=100, vx_mm_s=5.0, vy_mm_s=0.0)])
    v = kinematics.per_frame_speeds(tracks, window_frames=9)
    assert not np.isnan(v).any()
    assert len(v) == 2 * (100 - 8), "each track loses (w - 1) / 2 = 4 rows at each end"
    assert np.isclose(v, 3.0).sum() == 92 and np.isclose(v, 5.0).sum() == 92, "tracks were mixed"


@pending
def test_noise_of_a_still_object():
    rng = np.random.default_rng(2)
    still = pd.DataFrame({"t_s": np.arange(2000) / 240.0,
                          "x_mm": 4.0 + rng.normal(0, 0.006, 2000), "y_mm": -1.0 + rng.normal(0, 0.006, 2000)})
    assert kinematics.position_noise_mm(still) == pytest.approx(0.006, rel=0.05)


def track_with_bad_frames():
    """A shrimp at 4.8 mm/s for 721 frames; in frames 241-243 the autotracker sat 3.5 mm away."""
    t = straight_track("A", n_frames=721, vx_mm_s=4.8, vy_mm_s=0.0)
    bad = t["frame"].between(241, 243)
    t.loc[bad, "x_mm"] += 3.5
    return t


@pending
def test_jumps_are_found():
    assert list(kinematics.find_jumps(track_with_bad_frames())) == [241, 244]
    assert len(kinematics.find_jumps(straight_track())) == 0


@pending
def test_split_at_jumps_removes_the_bad_frames():
    tracks = pd.concat([track_with_bad_frames(), straight_track("B", y0=5.0)])
    out = kinematics.split_at_jumps(tracks, max_speed_mm_s=100.0, min_frames=24)
    assert sorted(out["track_id"].unique()) == ["A.1", "A.2", "B"]
    assert not out[out["track_id"].str.startswith("A")]["frame"].between(241, 243).any()
    assert len(out) == 721 - 3 + 240
