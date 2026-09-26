# Instructions for the AI coding agent

You are helping a group of undergraduate physics students, most of them new to programming, build a tracker for brine shrimp nauplii filmed in slow motion with a phone. Explain what you do in plain language, and keep changes small enough for a beginner to read.

## The project
- Input: a ~1-minute slow-motion video (120–240 fps) of a 35 mm petri dish seen from above, plus calibration values in `data/manifest.csv`.
- Output: one track per shrimp and physics results: speed distribution, stroke frequency, body length, Reynolds number. Later: mean squared displacement, a Lévy-flight test, and changes with age.
- Code lives in `src/shrimp/`, one module per role: `calibrate.py` (A), `detect.py` (B), `track.py` (C), `analyze.py`, `synthetic.py`, `validate.py` (D).
- `src/shrimp/video.py` is provided by the course and tested. Use it; do not modify it.

## Hard rules
1. Never load a whole video into memory. Read frames one at a time with `shrimp.video.iter_frames` (one minute of 1080p at 240 fps is about 30 GB as raw frames).
2. Real time comes from `fps_true` in `data/manifest.csv` (the students' stopwatch calibration). Never use the frame rate stored in the video file for physics.
3. Image coordinates: `x_px` increases to the right and `y_px` increases downward; the pixel in row r, column c has its center at (x = c, y = r). Use this everywhere, including angles.
4. Use the column names in `src/shrimp/formats.py`, with units in the names (`_px`, `_mm`, `_um`, `_s`, `_deg`). Do not change the formats unless the student says the whole group agreed.
5. Tests first. Before writing a function, make sure a test in `tests/` describes what it must do. Expected values must come from physics or from inputs whose answer is known (a drawn frame, a known trajectory, a synthetic video), never from running the code and copying its output.
6. Never delete, skip, or loosen a test to make it pass, and never change an expected value to match the output. If a test looks wrong, stop and explain why to the student. The only allowed change is deleting a `@pending` line once the function exists and its tests pass.
7. Run `uv run pytest` after every change and report the result.
8. Only edit the files needed for the task you were given. Ask before adding a package; then use `uv add <package>`. Allowed: numpy, scipy, pandas, matplotlib, opencv, scikit-image, trackpy.
9. Never add videos or large data files to git. Save figures to `results/figures/` and big tables or overlay videos to `results/work/` (ignored by git).
10. Never run `git push --force`, `git reset --hard`, or commands that delete branches or files outside this repository.
11. Finish every task by saying what you changed, how you verified it, and what you are unsure about.

## Commands
- Install or update packages: `uv sync`
- Run the tests: `uv run pytest`
- Check a video: `uv run python -m shrimp.check_video "path/to/video"`
