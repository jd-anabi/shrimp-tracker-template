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

## The same shrimp A seen by SAM 2 and EdgeTAM (`sam2/A.csv`, `edgetam/A.csv`)

Written the way `shrimp.segment` writes its results: the same frames as `A.csv` (120-2999), the columns
t, frame, x, y, pixelx, pixely, and empty x and y where the model lost the shrimp (EdgeTAM: frames
1800-1803). A model's outline includes the beating antennae, so its center is not the point Tracker
follows. Here it sits a fixed distance toward the head (SAM 2: 0.045 mm, EdgeTAM: 0.060 mm), wobbles
back and forth along the body at the stroke frequency (amplitude 0.025 and 0.030 mm), and has its own
noise (0.008 and 0.012 mm in x and in y).

What `uv run python -m shrimp.compare tools data/example A` finds:
- n_frames: 2877 (Tracker skipped 3 frames), 2880 (SAM 2), 2876 (EdgeTAM lost 4).
- Mean speed close to 4.0 mm/s and stroke frequency close to 8.5 Hz (period close to 0.118 s) for all three tools.
- RMS difference from Tracker close to sqrt(s^2 + A^2/2 + 2 sigma_tool^2 + 2 sigma_Tracker^2):
  0.050 mm for SAM 2 and 0.066 mm for EdgeTAM (s = shift, A = wobble amplitude, sigma = noise).
- Bias much smaller than the shift (about 0.01 mm): the shift points along the heading, and this shrimp
  swims back and forth, so the mean difference vector nearly cancels.
- These tracks are every frame (step size 1). Their velocities, and even more their accelerations, are
  dominated by noise: sigma_v = sigma / (sqrt(2) dt) = 1.0 mm/s and sigma_a = sqrt(14) sigma / (7 dt^2) = 185 mm/s^2
  for Tracker's sigma = 0.006 mm. That is why you track with step size 2 (sigma_v 0.5 mm/s, sigma_a 46 mm/s^2).

For the many-shrimp comparison between ages, see `data/example_day3/README.md`.
