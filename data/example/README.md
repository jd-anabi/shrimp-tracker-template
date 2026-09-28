# Example data: synthetic shrimp with known physics

These files were made by a computer, not by Tracker, but they are written the way Tracker exports
a point mass (File > Export > Data: columns t, frame, x, y; Full Precision; comma delimiter).
`E.txt` uses tabs and Tracker's default extension. Use these files to develop your code and to
check it: the answers are below.

The "video": fps_true = 240.0 exactly. Tracker's clip starts at frame 120 (so Tracker's t is 0 at
frame 120), and the tracks run from frame 120 to frame 2999 (12 s). Positions are in mm, origin at
the center of a 35 mm dish, y up. Each shrimp swims at v(t) = V (1 + 0.6 sin 2 pi f t) along a
slowly turning path and turns around before reaching 15 mm from the center. Every position has
independent noise of 0.006 mm (6 um) in x and in y.

| file | V (mm/s) | f (Hz) | what happened |
|---|---|---|---|
| A.csv | 4.0 | 8.5 | frames 700-702 were skipped (no rows) |
| B.csv | 5.0 | 9.0 | in frames 1500-1502 the autotracker jumped 1.2 mm, to a neighbour |
| C.csv | 6.0 | 9.5 | ends at frame 1200: it touched another shrimp |
| C2.csv | 6.0 | 9.5 | the same shrimp, picked up again from frame 1260 |
| D.csv | 3.0 | 8.0 | |
| E.txt | 4.5 | 9.0 | tab-separated, saved with Tracker's default extension |
| F.csv | 5.5 | 10.0 | |
| extra/still.csv | 0 | | a cyst stuck to the dish at (8, -6) mm, 5 s, noise 0.006 mm |
| extra/A_manual.csv | | | shrimp A marked by hand in frames 400-599: the clicks scatter by 0.020 mm in x and in y, and sit (0.030, -0.020) mm from the autotracked point |
| extra/body_lengths.csv | | | 10 lengths drawn around 0.47 +/- 0.03 mm |

What a correct analysis finds (window w = 9 frames, tracks of at least 1 s):
- 7 files. B splits at its jump into B.1 and B.2, so there are 8 tracks: A, B.1, B.2, C, C2, D, E, F.
- Mean speed of each track close to its V; the mean over the 8 tracks is close to
  (4.0 + 5.0 + 5.0 + 6.0 + 6.0 + 3.0 + 4.5 + 5.5) / 8 = 4.875 mm/s.
- Stroke frequency of each track close to its f, within the resolution 1/T; the mean over the
  8 tracks is close to 9.06 Hz.
- Tracking noise of the still object: close to 0.006 mm.
- A vs. A_manual in frames 400-599: 200 frames in common, bias close to 0.036 mm (the length of
  (0.030, -0.020)), RMS difference close to sqrt(0.036^2 + 2 (0.020^2 + 0.006^2)) = 0.047 mm.
- Body length: mean and SD of the 10 values in the file.
