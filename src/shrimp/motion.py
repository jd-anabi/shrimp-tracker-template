"""Role B: velocity and acceleration along a track, with Tracker's own formulas.

Tests: tests/test_motion.py. Build it with your agent (tests first!).

Rows of a track are steps: every k-th frame (Tracker's Clip Settings step size). With dt = the time
between consecutive steps (from t_s), Tracker computes
    v_n = (r_{n+1} - r_{n-1}) / (2 dt)
    a_n = (2 r_{n+2} - r_{n+1} - 2 r_n - r_{n-1} + 2 r_{n-2}) / (7 dt^2)
for r = x and for r = y. The second formula is the curvature of the parabola fitted to 5 points; it is
exact for constant acceleration. Using the same formulas for all three tools (Tracker, SAM 2,
EdgeTAM) makes their velocities and accelerations comparable.
"""

from __future__ import annotations

import pandas as pd


def velocity_acceleration(track: pd.DataFrame) -> pd.DataFrame:
    """Velocity and acceleration along ONE track (rows in time order, columns of formats.TRACK_COLUMNS).

    Returns a copy of `track` with five more columns: vx_mm_s, vy_mm_s, speed_mm_s (= |v|),
    ax_mm_s2, ay_mm_s2. The step is the most common difference between consecutive frame numbers.
    A value is NaN when a point it needs is missing: the first and last row for v, the first two
    and last two rows for a, and next to frames that were not tracked (never treat the rows on either
    side of a gap as neighbours: that fakes a jump in v and a).
    """
    raise NotImplementedError
