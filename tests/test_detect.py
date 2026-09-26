"""Role B tests. Fake shrimp are drawn at positions we choose, so we know the right answer.

Until a function is written it raises NotImplementedError and its tests show as "xfailed".
Once it exists the tests run for real. When they pass, delete the @pending line above them.
"""

import numpy as np
import pytest

from shrimp import detect
from shrimp.formats import DETECTION_COLUMNS

pending = pytest.mark.xfail(raises=NotImplementedError, strict=False, reason="not written yet")


def draw_ellipse(img, cx, cy, a, b, angle_deg, value, supersample=8):
    """Draw an anti-aliased filled ellipse whose center (cx, cy) can be between pixels.

    Pixel (row r, column c) has its center at (x = c, y = r), as in shrimp.formats.
    """
    h, w = img.shape
    yy, xx = np.mgrid[0:h * supersample, 0:w * supersample]
    x = (xx + 0.5) / supersample - 0.5
    y = (yy + 0.5) / supersample - 0.5
    th = np.deg2rad(angle_deg)
    u = (x - cx) * np.cos(th) + (y - cy) * np.sin(th)
    v = -(x - cx) * np.sin(th) + (y - cy) * np.cos(th)
    inside = (u / a) ** 2 + (v / b) ** 2 <= 1.0
    cover = inside.reshape(h, supersample, w, supersample).mean(axis=(1, 3))
    img[:] = img * (1 - cover) + value * cover


def _scene(shrimp, cysts=()):
    background = np.full((120, 200), 200.0)
    for cx, cy, r in cysts:  # static objects are in the background too
        draw_ellipse(background, cx, cy, r, r, 0, value=90)
    frame = background.copy()
    for cx, cy, a, b, angle in shrimp:
        draw_ellipse(frame, cx, cy, a, b, angle, value=60)
    return np.round(frame).astype(np.uint8), np.round(background).astype(np.uint8)


@pending
def test_two_shrimp_found_at_subpixel_positions():
    truth = [(50.3, 40.7, 9, 4, 0), (140.6, 80.2, 9, 4, 30)]
    frame, background = _scene(truth)
    det = detect.detect_shrimp(frame, background, min_area_px=30, max_area_px=500)
    assert set(DETECTION_COLUMNS) <= set(det.columns)
    assert len(det) == 2
    found = det.sort_values("x_px")[["x_px", "y_px"]].to_numpy()
    assert np.abs(found - np.array([[50.3, 40.7], [140.6, 80.2]])).max() < 0.5


@pending
def test_body_length_is_the_full_major_axis():
    frame, background = _scene([(100.0, 60.0, 9, 4, 20)])  # semi-axes 9 and 4 px
    det = detect.detect_shrimp(frame, background, min_area_px=30, max_area_px=500)
    assert det["length_px"].iloc[0] == pytest.approx(18.0, rel=0.15)
    assert det["width_px"].iloc[0] == pytest.approx(8.0, rel=0.25)


@pending
def test_static_cysts_are_not_shrimp():
    frame, background = _scene([(30.0, 30.0, 9, 4, 0)], cysts=[(100, 60, 4), (160, 90, 4)])
    det = detect.detect_shrimp(frame, background, min_area_px=30, max_area_px=500)
    assert len(det) == 1
    assert det["x_px"].iloc[0] == pytest.approx(30.0, abs=0.5)


@pending
def test_area_limits_reject_specks():
    frame, background = _scene([(60.0, 60.0, 9, 4, 0), (150.0, 30.0, 1.2, 1.2, 0)])
    det = detect.detect_shrimp(frame, background, min_area_px=30, max_area_px=500)
    assert len(det) == 1
