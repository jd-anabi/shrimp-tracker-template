# Report: brine shrimp at 1 and 3 days old (due Sunday Oct 4, 11:59 pm)

TEMPLATE: copy this file to `results/<your name>/REPORT.md` and fill in your copy. Use your own data. This is an
individual report.

Figures: the `shrimp.compare` commands save theirs in `results/<your name>/figures/` (`tools_A.png`,
`ages_edgetam.png`, ...). Put any other figure (a photo of your setup) in the same folder, and show each one with a
link relative to this file, e.g. `![three tools](figures/tools_A.png)`.

To hand it in, upload the **whole folder** `results/<your name>/` to your group's folder in the shared Google Drive,
next to your slides. Not just this file: `figures/` must sit next to `REPORT.md`, or the report shows no figures.

Most numbers are printed by `uv run python -m shrimp.compare tools ...` and `... ages ...` (README section 6).

Name: ___  Group: ___  Role: ___

## 1. Introduction
What you measured and why, in 2-4 sentences.

## 2. Setup and videos
A photo of the setup. For each video (1 and 3 days old): file name, age (hours since hatching), fps_true
(from the stopwatch clip: which frames, which readings), scale (calibration stick, and the tape-measure
check), Tracker's step size, dish size, water depth, temperature. Anything unusual.

## 3. Three tools on the best shrimp (1 day old)
- Which shrimp, which frames (first, last, step), and why you chose it.
- Figure: x, y, vx, vy, ax, ay and speed vs. time for Tracker, SAM 2 and EdgeTAM:
  `![three tools](figures/tools_A.png)`.
- Table: mean speed, stroke frequency and period, and the RMS difference and bias from Tracker, for each
  tool. How long each tool took you (setting up, running, checking).
- **How SAM 2 and EdgeTAM give a position, and why it differs from Tracker's** (one paragraph): the model
  returns the shrimp's outline; the script takes the center of the outline (the mean position of its
  pixels) and converts it to mm with your Tracker calibration, while Tracker's autotracker follows the
  point you clicked. The outline includes the beating antennae. Where does that put its center, how does
  the center move during a stroke, and what does that do to the speed, the acceleration, and the RMS
  difference and bias you measured?
- Why the acceleration is much noisier than the velocity (Tracker's formulas and the step size).
- Your favorite tool, and why (accuracy, failures, time, effort).

## 4. At least 10 shrimp of each age (with your favorite tool)
- Tool, number of shrimp of each age, about how long each was tracked, and anything you left out and why
  (collisions, an outline that switched shrimp).
- Histograms of average speed, stroke frequency and stroke period, both ages, with mean +/- SD and n:
  `![two ages](figures/ages_edgetam.png)` (`ages_tracker.png` or `ages_sam2.png` if that is your tool).
- Table: mean +/- SD for each age, the difference, and Welch's t, degrees of freedom and p.
- Is each difference significant at the 0.05 level? Say in words what p means here, and why the sample
  is shrimp, not frames. (The frequency and period tests are not independent: T = 1/f.)

## 5. Discussion and limitations
What else differs between the two videos besides age (dish, temperature, light, time of day, tool), how
it could bias the comparison, and what you would change next week.

## 6. Code and AI agent
The functions you wrote (your role), what you asked the agent, how you checked the results, and your pull
requests (authored and reviewed).
