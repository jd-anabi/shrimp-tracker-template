"""Tables passed between the roles. Change these only if the whole group agrees.

Conventions (everyone, every module):
    * One track = one shrimp followed without a doubt about which shrimp it is = one point
      mass in Tracker, exported to one file. If you are no longer sure which shrimp is which
      (two shrimp touched, one crossed another), end the point mass at the last frame you are
      sure of; if you can follow that shrimp again, continue in a new point mass (A2, A3, ...).
    * Positions are in mm, in Tracker's axes: origin at the CENTER OF THE DISH, x to the
      right, y UP (Tracker's default; the opposite of image rows).
    * frame is the video frame number (Tracker's "frame" column). Real time is
      t_s = frame / fps_true, where fps_true comes from the stopwatch clip
      (data/manifest.csv), never from the video file.
    * Units are in the column names: _mm, _s, _hz, _mm_s.
    * Tables are pandas DataFrames, one row per shrimp per tracked frame, in time order
      within each track.
"""

# One row per shrimp per tracked frame (Role A -> everyone)
TRACK_COLUMNS = [
    "track_id",  # str, the file name without its extension, e.g. "A", "B", "A2"
    "frame",     # int, video frame number
    "t_s",       # float, real time (s) = frame / fps_true
    "x_mm",      # float, position (mm), to the right
    "y_mm",      # float, position (mm), UP
]

# Columns every file exported from Tracker must contain. Tracker always writes t first;
# choose frame, x and y under "Columns" in File > Export > Data.
TRACKER_COLUMNS = ["t", "frame", "x", "y"]
