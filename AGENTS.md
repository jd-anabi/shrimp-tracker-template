# Instructions for the AI coding agent

You are helping a group of undergraduate physics students, most of them new to programming, write the analysis of brine shrimp nauplii tracked in slow-motion phone videos. Explain what you do in plain language, and keep changes small enough for a beginner to read.

## The project
- Each student tracks shrimp in two videos (1 day old and 3 days old) and exports one file per shrimp. Tools: **Tracker** (physlets.org/tracker) and the AI models **SAM 2** and **EdgeTAM**, which run through the provided script `src/shrimp/segment.py` and write files in the same format as Tracker.
- The analysis: on the best shrimp, compare the three tools (x, y, vx, vy, ax, ay and speed vs. time; stroke frequency and period); with at least 10 shrimp of each age, compare the ages (average speed, stroke frequency and period: mean ± SD, Welch's t-test).
- Data: `data/tracks/<video name>/<student>/` holds one file per track (`A.csv`, `A2.csv`, `B.csv`, ...) exported from Tracker; `sam2/` and `edgetam/` inside it hold the files written by `segment.py`; `extra/` holds anything that is not a track (e.g. `extra/start.csv`, one mark per shrimp, several point masses in one file). `data/manifest.csv` gives each video's `fps_true`. `data/example/` (1 day old, with `sam2/` and `edgetam/` versions of shrimp A) and `data/example_day3/` (3 days old) are synthetic tracks whose answers are known (see their README files).
- What a Tracker export looks like is described at the top of `src/shrimp/load.py` and in `data/example_day3/README.md`.
- Code lives in `src/shrimp/`, one role per student: `load.py` (A), `kinematics.py` and `motion.py` (B), `strokes.py` and `stats.py` (C), `validate.py` and `compare.py` (D). Needed this week: the functions listed in README section 6; the others (`fps_from_stopwatch`, `load_manifest`, `per_frame_speeds`, `position_noise_mm`, `reynolds_number`, `synthetic.py`, `report.py`) are not.
- `video.py`, `convert.py`, `segment.py`, `_edgetam.py`, and the command-line part of `compare.py` (below the line "PROVIDED") are provided by the course and tested. Do not modify them.

## Hard rules
1. Real time is `t_s = frame / fps_true`, with `fps_true` from `data/manifest.csv` (the students' stopwatch calibration). Never use Tracker's `t` column, the frame rate stored in a video file, or an assumed 240 fps for physics. Frames can be missing inside a track (tracked every 2nd frame, skipped, or lost): always take time differences from `t_s`, and never treat the rows on either side of a gap as neighbours.
2. Positions are in mm in Tracker's axes: origin at the center of the dish, x to the right, **y up**. Never flip y or convert to pixels.
3. Use the column names in `src/shrimp/formats.py`, with units in the names (`_mm`, `_s`, `_hz`, `_mm_s`, `_mm_s2`). Do not change the formats unless the student says the whole group agreed.
4. Statistics: the sample is shrimp, not frames. Each shrimp gives one value (pieces `A`, `A2`, `A.1` are one shrimp). Never use frames as independent samples.
5. Use the same formulas for every tool (Tracker, SAM 2, EdgeTAM): the tools differ in where they put the shrimp, not in how speed is computed.
6. Tests first. Before writing a function, make sure a test in `tests/` describes what it must do. Expected values must come from physics or from inputs whose answer is known (a straight line at a known speed, a known oscillation, a synthetic track), never from running the code and copying its output.
7. Never delete, skip, or loosen a test to make it pass, and never change an expected value to match the output. If a test looks wrong, stop and explain why to the student. The only allowed change is deleting a `@pending` line once the function exists and its tests pass.
8. Run `uv run pytest` after every change and report the result.
9. Only edit the files needed for the task you were given. Ask before adding a package; then use `uv add <package>`. Allowed: numpy, scipy, pandas, matplotlib. PyTorch and transformers are only for `segment.py`, through `uv run --with ...`: never add them to the project.
10. Never modify, move or delete files in `data/tracks/`, `data/example/` or `data/example_day3/`: they are measurements. If a file looks wrong, tell the student; they export it again from Tracker or run the script again.
11. Never add videos or large files to git. Save figures to `results/<student>/figures/` (or `results/figures/`) and big tables to `results/work/` (ignored by git).
12. Figures: use matplotlib and save them to files (`fig.savefig(...)`); do not call `plt.show()` in code that runs from the terminal or the tests. Label every axis with its unit.
13. Do not run `shrimp.segment` yourself: it takes minutes to hours. The student runs it.
14. Never run `git push --force`, `git reset --hard`, or commands that delete branches or files outside this repository.
15. Finish every task by saying what you changed, how you verified it, and what you are unsure about.

## Commands
- Install or update packages: `uv sync`
- Run the tests: `uv run pytest`
- Compare the three tools on one shrimp: `uv run python -m shrimp.compare tools <folder> <name>` (example: `uv run python -m shrimp.compare tools data/example A`)
- Compare two ages: `uv run python -m shrimp.compare ages <folder 1 day> <folder 3 days>` (example: `uv run python -m shrimp.compare ages data/example data/example_day3`)
- SAM 2 / EdgeTAM (the student runs it): `uv run --with torch --with transformers==5.18.0 --with timm python -m shrimp.segment <video>_tracker.mp4 <export.csv> --model edgetam`
- Check a video: `uv run python -m shrimp.check_video "path/to/video"`
