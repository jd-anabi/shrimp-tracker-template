# Instructions for the AI coding agent

You are helping a group of undergraduate physics students, most of them new to programming, write the analysis of brine shrimp nauplii tracked in a slow-motion phone video. Explain what you do in plain language, and keep changes small enough for a beginner to read.

## The project
- The students tracked each shrimp by hand and with the autotracker in **Tracker** (physlets.org/tracker) and exported one file per shrimp. This code reads those files and computes physics: speed distribution, stroke frequency, body length, Reynolds number. Later: mean squared displacement, a Lévy-flight test, and changes with age.
- Data: `data/tracks/<video name>/` holds one Tracker file per track (`A.csv`, `A2.csv`, `B.csv`, ...), plus `extra/still.csv` (a still object), `extra/A_manual.csv` (shrimp A marked by hand) and `extra/body_lengths.csv`. `data/manifest.csv` gives each video's `fps_true`. `data/example/` has the same layout with synthetic tracks whose physics is known (see its README).
- What a Tracker export looks like is described at the top of `src/shrimp/load.py`.
- Code lives in `src/shrimp/`, one module per role: `load.py` (A), `kinematics.py` (B), `strokes.py` (C), `synthetic.py`, `validate.py`, `report.py` (D).
- `src/shrimp/video.py` and `src/shrimp/convert.py` are provided by the course and tested. Do not modify them.

## Hard rules
1. Real time is `t_s = frame / fps_true`, with `fps_true` from `data/manifest.csv` (the students' stopwatch calibration). Never use Tracker's `t` column, the frame rate stored in a video file, or an assumed 240 fps for physics. Frames can be missing inside a track: always take time differences from `t_s`.
2. Positions are in mm in Tracker's axes: origin at the center of the dish, x to the right, **y up**. Never flip y or convert to pixels.
3. Use the column names in `src/shrimp/formats.py`, with units in the names (`_mm`, `_s`, `_hz`, `_mm_s`). Do not change the formats unless the student says the whole group agreed.
4. Tests first. Before writing a function, make sure a test in `tests/` describes what it must do. Expected values must come from physics or from inputs whose answer is known (a straight line at a known speed, a known oscillation, a synthetic track), never from running the code and copying its output.
5. Never delete, skip, or loosen a test to make it pass, and never change an expected value to match the output. If a test looks wrong, stop and explain why to the student. The only allowed change is deleting a `@pending` line once the function exists and its tests pass.
6. Run `uv run pytest` after every change and report the result.
7. Only edit the files needed for the task you were given. Ask before adding a package; then use `uv add <package>`. Allowed: numpy, scipy, pandas, matplotlib.
8. Never modify, move or delete files in `data/tracks/` or `data/example/`: they are measurements. If a file looks wrong, tell the student; they fix it in Tracker and export it again.
9. Never add videos or large files to git. Save figures to `results/figures/` and big tables to `results/work/` (ignored by git).
10. Figures: use matplotlib and save them to files (`fig.savefig(...)`); do not call `plt.show()` in code that runs from the terminal or the tests. Label every axis with its unit.
11. Never run `git push --force`, `git reset --hard`, or commands that delete branches or files outside this repository.
12. Finish every task by saying what you changed, how you verified it, and what you are unsure about.

## Commands
- Install or update packages: `uv sync`
- Run the tests: `uv run pytest`
- Run the whole analysis on the example data: `uv run python -m shrimp.report example`
- Run it on a video: `uv run python -m shrimp.report <video file name as in data/manifest.csv>`
- Check a video: `uv run python -m shrimp.check_video "path/to/video"`
