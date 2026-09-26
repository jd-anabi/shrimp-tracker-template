"""Role D tests (synthetic videos). The generator must write a readable video that agrees with its own truth table.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import numpy as np
import pandas as pd
import pytest

from shrimp import synthetic, video
from shrimp.formats import TRUTH_COLUMNS

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


@pending
def test_video_and_truth_agree(tmp_path):
    path = tmp_path / "synth.mp4"
    truth = synthetic.make_synthetic_video(path, n_shrimp=3, n_frames=48, fps=240.0,
                                           width_px=200, height_px=160, seed=1)
    assert set(TRUTH_COLUMNS) <= set(truth.columns)
    assert len(truth) == 3 * 48 and truth["track_id"].nunique() == 3
    assert truth["x_px"].between(0, 199).all() and truth["y_px"].between(0, 159).all()
    info = video.probe(path)
    assert info.n_frames == 48
    assert info.fps_container == pytest.approx(240.0, rel=1e-3)


@pending
def test_same_seed_same_truth(tmp_path):
    kwargs = dict(n_shrimp=3, n_frames=48, fps=240.0, width_px=200, height_px=160, seed=7)
    a = synthetic.make_synthetic_video(tmp_path / "a.mp4", **kwargs)
    b = synthetic.make_synthetic_video(tmp_path / "b.mp4", **kwargs)
    pd.testing.assert_frame_equal(a, b)


@pending
def test_mean_speed_is_what_we_asked_for(tmp_path):
    fps, um_per_px = 240.0, 32.0
    truth = synthetic.make_synthetic_video(tmp_path / "s.mp4", n_shrimp=2, n_frames=480, fps=fps,
                                           width_px=640, height_px=480, um_per_px=um_per_px,
                                           speed_mm_s=5.0, seed=3)
    speeds = []
    for _, t in truth.sort_values("frame").groupby("track_id"):
        step_px = np.hypot(np.diff(t["x_px"]), np.diff(t["y_px"]))
        speeds.append(np.mean(step_px) * um_per_px / 1000 * fps)  # mm/s
    assert np.mean(speeds) == pytest.approx(5.0, rel=0.15)
