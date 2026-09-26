"""Tables passed between the roles. Change these only if the whole group agrees.

Conventions (everyone, every module):
    * x_px increases to the RIGHT, y_px increases DOWN (image rows).
      The pixel in row r, column c has its center at (x_px = c, y_px = r).
    * Units are in the column name: _px (pixels), _mm, _um, _s (seconds), _deg.
    * t_s is REAL time in seconds: t_s = frame / fps_true, where fps_true comes
      from the stopwatch calibration in data/manifest.csv, never from the file.
    * Tables are pandas DataFrames; save them as CSV in results/work/.
"""

# One row per detected shrimp per frame (Role B -> Role C)
DETECTION_COLUMNS = [
    "frame",      # int, frame index as delivered by shrimp.video.iter_frames
    "t_s",        # float, real time (s)
    "x_px",       # float, sub-pixel centroid, to the right
    "y_px",       # float, sub-pixel centroid, downward
    "area_px",    # float, area of the detected blob (pixels^2)
    "length_px",  # float, major axis of the blob
    "width_px",   # float, minor axis of the blob
    "angle_deg",  # float, orientation of the major axis
]

# Detections linked into tracks (Role C -> Role D); x_mm, y_mm added by Role A's functions
TRACK_COLUMNS = DETECTION_COLUMNS + [
    "track_id",   # int, same value for the same shrimp over time
    "x_mm",       # float, position in mm (same axes as x_px)
    "y_mm",       # float, position in mm (same axes as y_px)
]

# Ground truth written by the synthetic-video generator (Role D, validation)
TRUTH_COLUMNS = ["frame", "t_s", "track_id", "x_px", "y_px"]
