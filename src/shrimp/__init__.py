"""Brine shrimp analysis (Physics M180G, Fall 2026).

The shrimp are tracked in Tracker (physlets.org/tracker); this package analyzes the exported tracks.

Modules and who owns them:
    video.py        provided by the course (tested; do not change): read and check phone videos
    convert.py      provided by the course (tested; do not change): make a copy Tracker can open
    formats.py      column names and conventions shared by everyone
    load.py         Role A: Tracker files -> one clean table of tracks
    kinematics.py   Role B: speeds, smoothing, tracking noise, jumps
    strokes.py      Role C: stroke frequency, per-track summary, Reynolds number
    synthetic.py    Role D: fake tracks with known physics (validation)
    validate.py     Role D: comparing two trackings of the same shrimp (validation)
    report.py       Role D: every number and figure for the report, from one video
"""

__version__ = "0.2.0"
