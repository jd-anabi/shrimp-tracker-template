# Brine shrimp analysis (Physics M180G, Fall 2026)

Your group filmed brine shrimp nauplii in a petri dish in slow motion at **1 day old** (Tuesday) and **3 days old** (Thursday). Each of you, with your own data:
1. tracks the **best shrimp** (about 10 s of clean swimming) with three tools, **Tracker**, **SAM 2** and **EdgeTAM**, and compares them: x, y, vx, vy, ax, ay and speed vs. time (mm, s), and the stroke frequency and period;
2. picks a favorite tool and, with it, tracks **at least 10 shrimp of each age** (about 10 s each);
3. tests whether age changes the average speed and the stroke frequency and period (histograms, mean ± SD, significance).

The group writes the analysis code together, with an AI agent (Antigravity CLI), and you are responsible for checking that it is right. SAM 2 and EdgeTAM run through a script the course provides (section 3b).

- Slides for this lab: shared by the TA. The Discord and Google Drive links are in the slides, not on this page, because this page is public.
- Questions: Discord or email (section 8). The TA is in the lab Tuesdays and Thursdays, 1–3 pm.

| When | What |
|---|---|
| Before Tuesday's lab | install Tracker; at least one person per group finishes the whole setup (section 1) |
| Tue Sep 29, 1–3 pm | record the 1-day-old dish, copy the original off the phone, check it, convert it for Tracker, upload it (section 2) |
| Thu Oct 1, 1–3 pm | record the 3-day-old dish the same way; write the analysis with your group and the agent (sections 4–6) |
| Thu → Sun | each of you: the best shrimp with three tools; at least 10 shrimp of each age with your favorite tool (sections 3, 3b) |
| **Sun Oct 4, 11:59 pm** | hand in, **individually**: your Google Slides and your REPORT.md, in your group's folder in the shared Google Drive (section 7) |

Contents: [1. Setup](#1-one-time-setup) · [2. The videos](#2-the-videos-in-the-lab) · [3. Tracker](#3-tracking-in-tracker) · [3b. SAM 2 and EdgeTAM](#3b-sam-2-and-edgetam) · [4. Daily workflow](#4-how-we-work-every-time) · [5. The agent](#5-working-with-the-agent) · [6. Roles and the analysis](#6-roles-and-the-analysis) · [7. Hand in](#7-what-to-hand-in-due-sunday-oct-4-1159-pm) · [8. Help](#8-asking-for-help) · [9. Troubleshooting](#9-troubleshooting)

---

## 1. One-time setup

You need a laptop with Windows, macOS or Linux. Chromebooks and iPads will not work; tell the TA right away if that is all you have. Each step ends with a **checkpoint**: do not continue until it works.

### Step 1: Accounts
- A GitHub account: https://github.com/signup
- A **personal** Google account (Gmail). UCLA Google accounts cannot sign in to Antigravity.

### Step 2: Tracker
Download the installer for your system from https://opensourcephysics.github.io/tracker-website (free; Windows, macOS, Linux; the old address physlets.org/tracker also works) and run it.

**Checkpoint:** Tracker opens and shows an empty window with a toolbar.

### Step 3: Open a terminal
- Windows: Start menu, type `PowerShell`, open **Windows PowerShell**.
- macOS: press Cmd+Space, type `Terminal`, press Enter.
- Linux: open your Terminal app.

Type each command below into the terminal and press Enter. Paths with spaces need quotes: `cd "My Folder"`.

### Step 4: Install the tools

**Windows (PowerShell)**, one line at a time:
```
winget install --id Git.Git -e --source winget
winget install --id GitHub.cli -e --source winget
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
irm https://antigravity.google/cli/install.ps1 | iex
```

**macOS (Terminal)**:
```
xcode-select --install
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -fsSL https://antigravity.google/cli/install.sh | bash
```
Then install the GitHub CLI with the macOS installer from https://cli.github.com (or `brew install gh` if you already use Homebrew).

**Linux**: install `git` with your package manager (e.g. `sudo apt install git`), the GitHub CLI from https://github.com/cli/cli#installation, then:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

Close the terminal and open a new one, so it finds the new programs.

**Checkpoint:** each of these prints a version number:
```
git --version
gh --version
uv --version
```

### Step 5: Connect the terminal to GitHub
```
gh auth login
```
Choose: **GitHub.com** → **HTTPS** → **Yes** (authenticate Git) → **Login with a web browser**. Copy the one-time code, press Enter, paste the code in the browser.

**Checkpoint:** `gh auth status` says you are logged in.

### Step 6: Get your group's repository
One person per group, once:
1. Open the template: https://github.com/jd-anabi/shrimp-tracker-template
2. Click **Use this template** → **Create a new repository**. Owner: you. Name: `shrimp-group-<letter>`. Choose **Private**. Create.
3. In the new repository: **Settings** → **Collaborators** → add your teammates and the TA (`jd-anabi`).

Everyone (after accepting the invitation email):
```
cd Documents
gh repo clone <owner>/shrimp-group-<letter>
cd shrimp-group-<letter>
```

**Checkpoint:** `git status` says `On branch main`.

### Step 7: Install the Python packages and run the tests
```
uv sync
uv run pytest
```
The first `uv sync` downloads Python and the packages; it can take a few minutes.

**Checkpoint:** the last line has no `failed` (on the template: `25 passed, 50 xfailed`). "xfailed" tests are for functions nobody has written yet. Writing them is your job.

### Step 8: Start the AI agent
In your repository folder:
```
agy
```
Choose **Google OAuth**, sign in with your personal Google account in the browser, and paste the code it gives you back into the terminal. Then type:

> Read AGENTS.md and README.md and explain this project to me in five bullet points.

**Checkpoint:** it explains the project. Press Ctrl+C to quit.

### Step 9: SAM 2 and EdgeTAM (everyone, by Friday)
In your repository folder, after `git pull` (the script arrived on Oct 1):
```
uv run --with torch --with transformers==5.18.0 --with timm python -m shrimp.segment --selftest --model edgetam
uv run --with torch --with transformers==5.18.0 --with timm python -m shrimp.segment --selftest --model sam2
```
The first run downloads PyTorch and the model (a few hundred MB, a few minutes; later runs start at once). Each run tracks a made-up shrimp on your laptop for 20 frames and prints how long your own shrimp will take.

**Checkpoint:** both end with `OK` and a time estimate. Post the two estimates on Discord. Intel Macs: see section 9.

If any step fails, ask for help (section 8).

---

## 2. The videos (in the lab)

### Record
Slides 6–8 show the setup. In short: the whole 35 mm dish fills a landscape frame, lit evenly from below; a mm ruler lies **beside the dish with its marks at the height of the water** and stays in the frame; focus and exposure locked; Slo-mo at 240 fps; 60 s without touching the phone. Then, with the same settings, film a stopwatch on a second phone for about 10 s (the stopwatch clip).

Write down: time of recording, when the shrimp hatched (ask the TA), water depth, temperature, the dish's inner diameter.

**Thursday (3 days old):** the same setup, phone and settings, and a new stopwatch clip if you can (if not, use Tuesday's fps_true: same phone). Everything below is done again for the Thursday video: copy, check, convert, upload, a row in `data/manifest.csv`, and a Tracker calibration.

### Get the original file off the phone
Slo-mo mode records real 240 fps frames, and the original file on the phone keeps all of them (on a computer the original plays at normal speed: that is expected, it is the 240 fps file). But when a slow-motion video leaves the phone through an app or the share button, the phone usually "bakes in" the slow motion: the TA's own test video arrived as a 30 fps file whose first and last seconds play at normal speed and whose middle is slowed down 8 times. Every speed and frequency computed from such a file is wrong. So:

**Never upload a video from the phone's app (Drive, Messages, email, etc.). Copy the original to a computer first.**

- **iPhone:** first, Settings → Photos (or Settings → Apps → Photos) → **Transfer to Mac or PC** → **Keep Originals**. Then either:
  - Windows: connect with a cable, unlock the phone and tap **Trust**, open File Explorer → This PC → Apple iPhone → Internal Storage → DCIM, and copy the `.MOV` file; or
  - Mac: AirDrop the video, but first tap **Options** at the top of the share sheet and turn on **All Photos Data**; or
  - any computer: iCloud.com → Photos → select the video → Download → **Unmodified Originals**.
- **Android:** connect with a cable, choose "File transfer" on the phone, open DCIM → Camera and copy the video file.

Name the files with your group letter, the date and time, and what they are, e.g. `groupB_2026-09-29_1325_main.MOV`, `groupB_2026-09-29_1331_stopwatch.MOV`, and on Thursday `groupB_2026-10-01_1330_main.MOV`.

### Check it
In your repository folder (tip: drag the file onto the terminal window to paste its path):
```
uv run python -m shrimp.check_video "path/to/groupB_2026-09-29_1325_main.MOV"
```
It must end with `OK`. If it prints a `WARNING`, do not use the file: post the output on Discord.

### Convert it for Tracker
Tracker cannot open the HEVC (H.265) files iPhones record in slow motion. Make a copy it can open:
```
uv run python -m shrimp.convert "path/to/groupB_2026-09-29_1325_main.MOV"
uv run python -m shrimp.convert "path/to/groupB_2026-09-29_1331_stopwatch.MOV"
```
Each writes a `..._tracker.mp4` next to the original (a minute of video takes a few minutes). The copy is H.264 with every frame kept, in order, and the phone's rotation applied; it checks that the frame count and frame rate match the original. It is not re-timed: frame n of the copy is frame n of the original. SAM 2 and EdgeTAM use the same copy (section 3b).

### Upload
Upload the originals and the `_tracker.mp4` copies to your group's folder in the shared Google Drive (link in the slides). Videos never go into git (GitHub rejects files over 100 MB, and `.gitignore` refuses them). Each of you needs the `_tracker.mp4` copies on your own laptop.

---

## 3. Tracking in Tracker

What each of you tracks, for your own data (positions in **mm**, origin at the **center of the dish**, x to the right, **y up**):
- **The best shrimp** in the 1-day-old video: one shrimp swimming in open water for about **10 s**, not touching others or the wall. Track it in Tracker, then with SAM 2 and EdgeTAM (section 3b).
- **At least 10 shrimp of each age**, about 10 s each, with your favorite tool: in Tracker as below, or with SAM 2/EdgeTAM from one mark per shrimp (section 3b). Use the **same tool for both ages**: the tools do not measure the same point of the body (section 3b), so mixing them would fake an age effect.

Use **step size 2** (every 2nd frame, 120 positions per second, about 13 per stroke): it halves the work and makes velocities and accelerations much less noisy (slide on noise). Several of you may track the same shrimp, but in your own set each shrimp appears once. Shrimp you already tracked this week count: copy your own files into your folder.

### Once per video: calibrate and share (one person per group)
1. **Open** `..._main_tracker.mp4` in Tracker (File → Open File). Not the `.MOV`: Tracker cannot read it.
2. **fps_true**: open `..._stopwatch_tracker.mp4` in a second tab. Find two frames far apart (e.g. 10 s apart) and note each frame number (shown under the video) and the stopwatch reading. Then fps_true = (frame_b − frame_a) / (time_b − time_a). Your phone says 240; measure it anyway.
3. **Clip Settings** (film-strip button on the toolbar), in the main video's tab: frame rate = fps_true, **step size 2**.
4. **Calibration**: Calibration button → New → Calibration Stick. Shift-click two ruler marks far apart (e.g. 0 and 30 mm), click the stick's length and type the distance in **mm** (`30`, not `0.03`).
5. **Origin at the dish center**: measuring tools button (ruler icon) → Circle Fitter. Shift-click 4 or more points spread around the inner edge of the dish, then in the circle fitter's menu choose **Move Origin to Center**. Show the axes (Axes button): x to the right and y up (leave Tracker's default).
6. **Check the scale**: measuring tools → Tape Measure on two other ruler marks (e.g. 5 and 25 mm): it must read 20.0 mm within 1%. If not, redo the calibration stick.
7. **Save** (File → Save Tab As) as `groupB_2026-09-29_1325_main.trk` in the same folder as the video, and upload the `.trk` to your group's Drive folder. Everyone opens this `.trk` (keep it next to the video), so the whole group has the same calibration. Do the same for the Thursday video (its own `.trk`).

### Everyone: autotrack a shrimp
1. Open the group's `.trk`. **Create** (toolbar) → **Point Mass**. Rename it: Track menu → the point mass → Name... → `A` (your best shrimp; then `B`, `C`, ...).
2. Turn off **Auto-refresh** (Refresh button on the toolbar → uncheck Auto-refresh): autotracking is much faster.
3. Open the **Autotracker** (toolbar button). Go to the first frame. **Shift+Ctrl+click** the shrimp (Mac: Shift+Cmd+click): this is the key frame. Make the template a small box around the body, and the search area a little larger than one step's move.
4. Click **Search**. It marks the shrimp step after step.
5. It stops when the match is weak (usually two shrimp touching, or the wall). If the mark is on your shrimp, **Accept**. If not, shift-click your shrimp to mark it by hand. **Skip** leaves one frame unmarked.
6. **Not sure which shrimp it is?** Go back to the last frame you are sure of and use Delete → Later Points: the point mass ends there. If you can pick the same shrimp up again with certainty, continue in a new point mass named `A2` (then `A3`, ...). Never guess: a track that jumps to another shrimp ruins its speed.
7. **Check**: play the track back, and look at the x and y plots: a spike is a jump. Delete wrong marks the same way.

### Export: one point mass per file
File → Export → Data. In the Export Data window:
- **Tracks**: click the button and tick **one** point mass (e.g. `A`);
- **Columns**: `frame`, `x`, `y`, `pixel x`, `pixel y` (Tracker always adds `t` first; SAM 2 and EdgeTAM need the pixel columns);
- **Number Format**: Full Precision; **Delimiter**: Comma.

Click **Save As...** and save it as `A.csv` in your folder (below). The file name is the track's name: `A2.csv`, `B.csv`, ... Tracker writes a row for every frame, even with step size 2; the rows of skipped frames only have `t`, and the code drops them.

### Where the files go
In the repository, one folder per video, named like the video without its extension, and in it **one folder per student** (your first name, lowercase):
```
data/tracks/groupB_2026-09-29_1325_main/          1 day old
    groupB_2026-09-29_1325_main.trk               the group's Tracker file (calibration)
    ana/                                          Ana's data
        A.csv                                     her best shrimp, from Tracker
        sam2/A.csv  edgetam/A.csv                 the same shrimp, from shrimp.segment (section 3b)
        B.csv  C.csv  ...                         more shrimp, if Tracker is her favorite tool
        extra/start.csv                           one mark per shrimp, if SAM 2 or EdgeTAM is her favorite
data/tracks/groupB_2026-10-01_1330_main/          3 days old
    groupB_2026-10-01_1330_main.trk
    ana/ ...                                      at least 10 shrimp, with the same tool
```
Every `.csv` or `.txt` file directly in a folder is read as a track, so keep anything else in `extra/`. These files are measurements: nobody edits them. To redo a track, export it again from Tracker (or run the script again).

---

## 3b. SAM 2 and EdgeTAM

SAM 2 and EdgeTAM are AI models from Meta: given a video and one click on an object, they find the object's **outline** (which pixels belong to it) in every frame. EdgeTAM is a smaller, faster version of SAM 2. Their web demos are not usable for this lab: the SAM 2 demo cuts the video to 10 s, shrinks it and resamples it to 24 frames per second, and both demos give back only a video with the outlines painted on, no positions.

So the course provides a script, `shrimp.segment` (tested; do not change it), that runs the models on your laptop and does what Tracker does internally:
1. reads your `_tracker.mp4` one frame at a time (the same frames Tracker uses);
2. asks the model for each shrimp's outline;
3. takes the center of the outline (the mean position of its pixels) as the shrimp's position;
4. converts pixels to mm with **your** Tracker calibration (read from your export's pixel and mm columns), and frames to seconds with fps_true;
5. saves one file per shrimp in the same format as a Tracker export, a slowed-down video with the outlines drawn on (`overlay.mp4`, for your slides; not in git), and `run.log`.

The outline includes the beating antennae, so its center is not the point Tracker's autotracker follows: it sits toward the head and wobbles at the stroke frequency. Your report explains this difference and what it does to the speed and acceleration.

### The best shrimp
After exporting `A.csv` from Tracker (with the pixel columns):
```
uv run --with torch --with transformers==5.18.0 --with timm python -m shrimp.segment "path/to/groupB_2026-09-29_1325_main_tracker.mp4" data/tracks/groupB_2026-09-29_1325_main/ana/A.csv --model edgetam
uv run --with torch --with transformers==5.18.0 --with timm python -m shrimp.segment "path/to/groupB_2026-09-29_1325_main_tracker.mp4" data/tracks/groupB_2026-09-29_1325_main/ana/A.csv --model sam2
```
The model starts where your Tracker track starts and follows the same frames, so the three tools can be compared frame by frame. Results: `ana/edgetam/A.csv` and `ana/sam2/A.csv`. Then compare the three (section 6):
```
uv run python -m shrimp.compare tools data/tracks/groupB_2026-09-29_1325_main/ana A
```
It saves the figure in Ana's report folder: `results/ana/figures/tools_A.png`.

### Many shrimp at once
1. In Tracker (the group's `.trk`), go to one frame where your shrimp are clearly apart. Create a point mass for each shrimp (`B`, `C`, ... up to at least `K`), and **shift-click each shrimp once, all on that same frame**.
2. File → Export → Data: **Tracks**: tick all of these point masses (not `A` if `A` already has a long track); same columns as above. Save as `extra/start.csv` in your folder: it is not a track.
3. Run the script on it for 10 s:
```
uv run --with torch --with transformers==5.18.0 --with timm python -m shrimp.segment "path/to/groupB_2026-09-29_1325_main_tracker.mp4" data/tracks/groupB_2026-09-29_1325_main/ana/extra/start.csv --model edgetam --seconds 10
```
It writes `B.csv`, `C.csv`, ... into `ana/edgetam/` (next to `extra/`), at step 2.
4. **Watch `overlay.mp4`.** Every outline must stay on its own shrimp. If one jumps to a neighbour or the wall, the script prints a `CHECK` line, and the analysis cuts the track at a jump; if an outline quietly switched shrimp, move that shrimp's file into `extra/` (it is then not read) and say so in your report.

### How long it takes
The script prints its progress and the time left. On a laptop, EdgeTAM needs roughly 5–10 min for one shrimp over 10 s at step 2, and about 30–45 min for 10 shrimp together; SAM 2 about 4 times longer. Your `--selftest` estimate is better than these numbers. Ctrl+C stops it and saves what was tracked so far. Apple-silicon Macs use their GPU when it works. Options: `--seconds`, `--step` (default: your Tracker track's), `--fps` (default: from `data/manifest.csv`), `--out`.

---

## 4. How we work (every time)

```
git switch main
git pull
git switch -c <yourname>-<what-you-are-doing>
agy
```
Work with the agent. When the tests pass and you have read the changes:
```
git status
git add src tests
git commit -m "Say what you changed, e.g. Compute speeds with a centered window"
git push -u origin HEAD
gh pr create --web
```
`gh pr create --web` opens the pull request page in your browser; answer the questions in the description (what you asked the agent, how you checked it). A teammate reviews the pull request on GitHub (**Files changed** → comment → **Approve**), then the author clicks **Merge**. Afterwards everyone runs `git switch main` and `git pull`.

Every pull request must pass the automatic tests (the green check on GitHub).

**Adding your data**: everyone adds their own folder, `data/tracks/<video name>/<your name>/` (layout in section 3), with `git add data/tracks`, in a pull request as above. `overlay.mp4` stays on your laptop (git refuses videos). Nobody edits these files afterwards: they are measurements.

---

## 5. Working with the agent

The agent reads `AGENTS.md` (the project rules) every time it starts. Your rules:
- Keep it in review mode, where it asks before changing files. Never switch to "always proceed".
- Start each task by asking for a plan. Then ask for tests first, then the code, then `uv run pytest`.
- Read every change before accepting it. You must be able to explain your module in lab.
- Use a Flash model by default (`/model`). Switch to Gemini 3.1 Pro or Claude only for hard problems: the free plan has weekly limits.
- Do not use `/boost` or `/teamwork-preview`; they run several agents at once and use up your limit.
- `/rewind` undoes the agent's last steps. Git undoes everything else.
- If you hit your weekly limit: switch to a Flash model, work with a teammate, and tell the TA.

---

## 6. Roles and the analysis

| Role | Files | Needed for Sunday |
|---|---|---|
| A. Import | `src/shrimp/load.py` | `read_tracker_csv`, `load_tracks`: Tracker's files into one clean table (mm, real time), with checks that catch a wrong frame rate or scale |
| B. Kinematics | `src/shrimp/kinematics.py`, `motion.py` | `compute_speed`, `find_jumps`, `split_at_jumps`; `velocity_acceleration` (vx, vy, ax, ay with Tracker's own formulas) |
| C. Strokes & statistics | `src/shrimp/strokes.py`, `stats.py` | `stroke_frequency_hz`, `summarize_tracks`; `per_shrimp`, `describe`, `welch_test` |
| D. Comparisons | `src/shrimp/validate.py`, `compare.py` | `compare_tracks`; `tool_comparison`, `tool_figure`, `age_comparison`, `age_figure` |

Not needed this week (leave them as they are, xfailed is fine): `fps_from_stopwatch`, `load_manifest`, `per_frame_speeds`, `position_noise_mm`, `reynolds_number`, `synthetic.py`, `report.py`.

Order: A's `read_tracker_csv` and B's `compute_speed` first; C's `summarize_tracks` uses `compute_speed`; D's functions use everyone's. Until those exist, work with the example data, whose answers are known: `data/example/` (1 day old, with SAM 2 and EdgeTAM versions of shrimp A) and `data/example_day3/` (3 days old); see their README files.

Groups of 3: one person does A and B. Groups of 5: split D into the tool comparison and the age comparison. The tables passed between roles are defined in `src/shrimp/formats.py`; change them only if the whole group agrees. `video.py`, `convert.py`, `segment.py` and `_edgetam.py` are provided and tested: use them, do not change them.

**Statistics, the one rule:** the sample is shrimp, not frames. Each shrimp gives one average speed, one stroke frequency and one period (pieces like `A` and `A2` are combined). Frames of the same shrimp are not independent, so treating them as samples makes any difference look significant. Welch's t-test compares the two ages without assuming equal spreads; a difference is significant if p < 0.05.

### Running the analysis
When the functions above pass their tests:
```
uv run python -m shrimp.compare tools data/example A
uv run python -m shrimp.compare ages data/example data/example_day3
```
These run on the example data, whose answers you know. Then on your own data (Ana, with EdgeTAM as her favorite tool):
```
uv run python -m shrimp.compare tools data/tracks/groupB_2026-09-29_1325_main/ana A
uv run python -m shrimp.compare ages data/tracks/groupB_2026-09-29_1325_main/ana/edgetam data/tracks/groupB_2026-10-01_1330_main/ana/edgetam
```
(With Tracker as your favorite, drop `/edgetam`.) fps_true comes from each video's row in `data/manifest.csv`. `tools` prints, for each tool, the mean speed, stroke frequency and period, and the RMS difference and bias from Tracker, and saves the figure of x, y, vx, vy, ax, ay and speed vs. time as `results/<your name>/figures/tools_A.png`. `ages` prints one row per shrimp for each age, the mean ± SD and Welch's test, and saves the histograms as `results/<your name>/figures/ages_edgetam.png` (named after the tool: `ages_tracker.png`, `ages_sam2.png`); it warns you if the two folders hold different tools. Your name comes from the folder (`.../ana/...` → `results/ana/`); the example data go to `results/figures/`. These are the figures your report shows (section 7).

---

## 7. What to hand in (due Sunday Oct 4, 11:59 pm)

**Individually** (your own data), in **your group's folder in the shared Google Drive** (link in the slides):
1. **Google Slides, 5–10 pages**, with your name in the file name: introduction, setup (a photo), a video example (e.g. your `overlay.mp4`), the three tools on the best shrimp (x, y, vx, vy, ax, ay and speed vs. time; frequency and period), your favorite tool and why, histograms of average speed, frequency and period for each age (mean ± SD), the effect of age with its significance (p), and a conclusion.
2. **Your report** (Markdown): copy `results/REPORT.md` to `results/<your name>/REPORT.md` and fill it in, with your figures in `results/<your name>/figures/`. Then upload the **whole folder** `results/<your name>/` to the same Drive folder, not just `REPORT.md`: `figures/` must sit next to `REPORT.md` there, or the report shows no figures.
3. **Your data** in `data/tracks/<video name>/<your name>/` in the repository, for both videos (section 3).

**As a group**, on the `main` branch: both videos' rows in `data/manifest.csv`; the functions in section 6 written, with their tests passing (no `@pending` left on them) and the green check on GitHub; each member authored at least one merged pull request and reviewed at least one.

---

## 8. Asking for help

Discord or email the TA (the links are in the lab slides). Always include:
- your operating system,
- the exact command you typed (or what you clicked in Tracker),
- the full error text (copy and paste, not just a photo),
- a screenshot,
- what you already tried.

The TA is in the lab Tuesdays and Thursdays 1–3 pm.

---

## 9. Troubleshooting

- **"not recognized" / "command not found"**: close and reopen the terminal. If it still fails, run the install line again.
- **`winget` not found (Windows)**: install Git from https://git-scm.com/download/win and the GitHub CLI from https://cli.github.com, then continue.
- **"running scripts is disabled" (Windows)**: use the uv install line exactly as written; it includes `-ExecutionPolicy ByPass`.
- **`uv sync` fails**: check your internet connection and run it again; if it still fails, post the full error.
- **`gh repo clone` says not found**: accept the invitation email first, and check the owner and name.
- **`git push` is rejected**: someone merged first. Run `git pull`, then push again. Ask for help if git mentions a conflict.
- **`check_video` prints a WARNING**: you have a re-timed copy. Redo section 2.
- **Tracker says the video could not be opened**: open the `_tracker.mp4` copy, not the `.MOV` (section 2).
- **The `.trk` opens without the video**: put the `.trk` in the same folder as the `_tracker.mp4`, or open the video again from File → Open File.
- **`load_tracks` says the time step does not match fps_true**: set the frame rate in Tracker's Clip Settings to fps_true, then export again.
- **`load_tracks` says a position is too far from the origin, or none is more than 1 mm from it**: the calibration stick's length was not typed in mm, or the origin is not at the center of the dish. Fix it in Tracker and export again.
- **`read_tracker_csv` says the file holds several point masses**: export one point mass per file (only `extra/start.csv` holds several).
- **Numbers in your files use commas for decimals (`1,52`)**: your computer's region settings leaked into the export. Choose a different delimiter than the comma and ask the TA.
- **`shrimp.segment` says there are no columns pixelx, pixely**: export again with the columns `pixel x` and `pixel y` ticked.
- **`shrimp.segment` says every shrimp must be marked on the same first frame**: in `extra/start.csv`, mark all of them on one frame.
- **`shrimp.segment` says fps_true is unknown**: add the video's row to `data/manifest.csv` (the `video_file` name must match the video), or give `--fps`.
- **Installing PyTorch fails on an Intel Mac**: PyTorch no longer supports Intel Macs. Run the script on a teammate's laptop with your video and your export: the results are still your data.
- **The script is too slow**: try fewer seconds (`--seconds 5`) or fewer shrimp per run, let it run overnight, or use Tracker as your favorite tool.
- **The agent says you reached a limit**: see section 5.
