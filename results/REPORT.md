# Group report: one video (due Monday Oct 5)

Group: ___  Members and roles: ___

Most numbers below are printed by `uv run python -m shrimp.report <your video>`; say which window w and which settings you used.

## 1. The video
File name, recording date and time, shrimp age (hours since hatching), phone, fps_true (from the stopwatch clip: which two frames, which readings), dish size, water depth, temperature. Anything unusual.

## 2. Tracking in Tracker
Calibration (which ruler marks, stick length) and the scale check (a different ruler interval measured with Tracker's tape measure). Where the origin is. Autotracker settings (template size, evolution rate, automark level). How many shrimp and frames you tracked, how you handled collisions and the wall, and how long it took.

## 3. Validation
- **Synthetic tracks** (`synthetic.py`): the settings you used, and the speed and stroke frequency your analysis recovers vs. the truth. Also the example data (`data/example/README.md`).
- **The same shrimp tracked twice** (`extra/A_manual.csv` vs. the autotracker, `validate.compare_tracks`): RMS difference, bias and largest difference. What causes each?
- **Tracking noise** σ of a still object (`extra/still.csv`), and the speed noise it predicts, σ_v = √2 σ / ((w − 1) Δt). Compare with the fast wiggles in your speed plots.
- **Jumps**: how many `find_jumps` found, and what you did about them. One figure of a track with its speed vs. time.

## 4. Physics
- Speed distribution: histogram, mean ± SD per frame and per track (`summarize_tracks`), and the window w. Why do the per-frame and per-track SDs differ?
- Stroke frequency: value ± frequency resolution, and how many tracks it comes from.
- Body length: mean ± SD in mm, and how many shrimp.
- Reynolds number, with the numbers you used.
- A figure of all tracks in the dish.

## 5. Limitations, and what you would change before the 7-day recordings

## 6. Who did what
One line per person: shrimp tracked, pull requests authored, pull requests reviewed.
