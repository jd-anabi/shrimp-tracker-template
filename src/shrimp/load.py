"""Role A: import and calibration. From the files exported by Tracker to one clean table of tracks.

Tests: tests/test_load.py. Build each function with your agent (tests first!).

What a file exported by Tracker (File > Export > Data, one point mass, comma delimiter,
Number Format "Full Precision") looks like:

    ,mass A,,,
    t,frame,x,y,
    0.000000E0,1.200000E2,-3.512840E0,4.100032E0,
    4.166667E-3,1.210000E2,-3.498114E0,4.101556E0,
    ...

The first line holds the point mass name, the second the column names. Every number, even the
frame number, may be in scientific notation. Lines may end with an extra delimiter.
"""

from __future__ import annotations

import pandas as pd


def fps_from_stopwatch(frame_a: int, time_a_s: float, frame_b: int, time_b_s: float) -> float:
    """True frame rate from two frames of the stopwatch clip.

    Note two frames far apart and the stopwatch reading in each (seconds):
    fps_true = (frame_b - frame_a) / (time_b_s - time_a_s). Raise ValueError if the times are equal.
    """
    raise NotImplementedError


def load_manifest(path: str = "data/manifest.csv") -> pd.DataFrame:
    """Read data/manifest.csv (one row per main video).

    Raise ValueError if the column video_file or fps_true is missing or has an empty cell, or
    if an fps_true is below 100 (a slow-motion original is 120-240 fps; about 30 means a
    re-timed copy or a typo).
    """
    raise NotImplementedError


def read_tracker_csv(path) -> pd.DataFrame:
    """Read one file exported from Tracker (one point mass) into the columns t, frame, x, y.

    Handle what Tracker writes (see the top of this file): a first line with the point mass
    name (it may be missing if the data were copied from the table instead), commas or tabs
    between columns, an extra delimiter at the end of lines, numbers in scientific notation
    (1.500000E-2), the frame number as a float (1.200000E2 -> 120). Return frame as int.
    Drop rows where x or y is empty (frames where the shrimp was not marked).
    Raise ValueError, saying what is wrong:
      * if t, frame, x or y is missing (choose the columns when exporting);
      * if the file holds more than one point mass (Tracker then writes "#multi:" and repeats
        the x and y columns): export one point mass per file.
    Extra columns (vx, v, ...) are ignored.
    """
    raise NotImplementedError


def load_tracks(folder, fps_true: float, max_radius_mm: float = 20.0) -> pd.DataFrame:
    """Read every .csv and .txt file directly in `folder` (one point mass each) into one table.

    Files in subfolders (e.g. extra/) are not read. Returns the columns in
    shrimp.formats.TRACK_COLUMNS: track_id is the file name without its extension,
    t_s = frame / fps_true (recomputed here, whatever Tracker's t says). Rows are sorted by
    track_id, then frame.
    Raise ValueError, naming the file, when a file cannot be right:
      * Tracker's time step per frame, (change in t) / (change in frame), differs from
        1 / fps_true by more than 1%: the frame rate in Tracker's Clip Settings was not fps_true.
        (Only the step matters: Tracker's t starts at 0 at the clip's start frame, which need
        not be frame 0.)
      * a position is more than max_radius_mm from the origin, or no position is more than
        1 mm from it: the calibration was not in mm, or the origin is not at the dish center.
    Raise FileNotFoundError if the folder has no .csv or .txt file.
    """
    raise NotImplementedError
