# Example data: synthetic 3-day-old shrimp (for the age comparison)

**These numbers are invented to test the code. They are not a prediction of what real 3-day-old
shrimp do: your own data decide that.**

Eight shrimp (A-H), written exactly as Tracker 6.3.5 exports a point mass with step size 2
(File > Export > Data: Columns frame, x, y, pixelx, pixely; Number Format Full Precision; Delimiter comma):
- the first line holds the name, the second the column names (with a comma at the end);
- the frame number is a whole number, everything else is in scientific notation;
- Tracker writes a row for EVERY frame, even with step size 2: the rows of the frames it skipped
  (97, 99, ...) hold only t. `read_tracker_csv` must drop them (x and y are empty).

The "video": fps_true = 240.0 exactly; Tracker's clip starts at frame 96 (t = 0 there); every shrimp
is tracked for 10 s (frames 96-2494, every 2nd frame). Positions in mm, origin at the dish center,
y up, noise 0.006 mm; 0.0324 mm per pixel. Each shrimp swims at v(t) = V (1 + 0.6 sin 2 pi f t):

| file | V (mm/s) | f (Hz) |
|---|---|---|
| A.csv | 4.0 | 7.0 |
| B.csv | 5.5 | 7.5 |
| C.csv | 6.0 | 6.5 |
| D.csv | 4.5 | 8.0 |
| E.csv | 3.5 | 7.0 |
| F.csv | 5.0 | 7.5 |
| G.csv | 6.5 | 7.0 |
| H.csv | 5.0 | 8.0 |

`extra/start.csv` shows what a many-shrimp start file for `shrimp.segment` looks like: all eight
shrimp marked once on frame 96 and exported together (Tracker writes "#multi:", a line of names,
and the columns repeated for each point mass). There is no video for it.

What `uv run python -m shrimp.compare ages data/example data/example_day3` finds (one value per
shrimp; `data/example` has 6 shrimp because B's pieces and C, C2 are combined):
- average speed: 1 day old close to 4.67 +/- 1.08 mm/s (mean +/- SD, n = 6), 3 days old close to
  5.00 +/- 1.00 mm/s (n = 8). Welch's test: p close to 0.6, **not significant**: with this many shrimp
  and this much spread, a 0.3 mm/s difference cannot be told from chance.
- stroke frequency: close to 9.00 +/- 0.71 Hz and 7.31 +/- 0.53 Hz; p below 0.01, **significant**.
- stroke period (one value 1/f per shrimp): close to 0.112 and 0.137 s; p below 0.01. The mean of the
  periods is not 1 / (mean frequency): it is never smaller (for the six true values: 0.1117 s,
  while 1 / 9.0 Hz = 0.1111 s).
