# Brine shrimp analysis (Physics M180G, Fall 2026)

Your group films 10–20 brine shrimp nauplii in a petri dish in slow motion, follows about 10 of them in **Tracker**, and writes Python code, with an AI agent (Antigravity CLI), that turns those tracks into physics: speed, stroke frequency, body length and Reynolds number. You are responsible for checking that the code is right.

- Slides for this lab: shared by the TA. The Discord and Google Drive links are in the slides (slides 4 and 10), not on this page, because this page is public.
- Questions: Discord or email (section 8). The TA is in the lab Tuesdays and Thursdays, 1–3 pm.

| When | What |
|---|---|
| Before Tuesday's lab | install Tracker; at least one person per group finishes the whole setup (section 1) |
| Tue Sep 29, 1–3 pm | record, copy the original off the phone, check it, convert it for Tracker, upload it (section 2) |
| Tue → Thu 1 pm | calibrate once per group, then everyone tracks their shrimp in Tracker and exports them (section 3) |
| Wed Sep 30, 11:59 pm | everyone's setup finished (section 1) |
| Thu Oct 1, 1–3 pm | write the analysis with your group and the agent (sections 4–6) |
| Mon Oct 5, 11:59 pm | hand in (section 7) |

Contents: [1. Setup](#1-one-time-setup) · [2. The video](#2-the-video-tuesday-in-the-lab) · [3. Tracker](#3-tracking-in-tracker-tuesday--thursday-1-pm) · [4. Daily workflow](#4-how-we-work-every-time) · [5. The agent](#5-working-with-the-agent) · [6. Roles](#6-roles) · [7. Hand in](#7-what-to-hand-in-due-monday-oct-5) · [8. Help](#8-asking-for-help) · [9. Troubleshooting](#9-troubleshooting)

---

## 1. One-time setup

You need a laptop with Windows, macOS or Linux. Chromebooks and iPads will not work; tell the TA right away if that is all you have. Each step ends with a **checkpoint**: do not continue until it works.

Deadlines: **Tracker** (step 2) before Tuesday's lab, because you track from Tuesday to Thursday. **At least one person per group** does every step before Tuesday's lab: they check and convert the video in the lab (section 2). Everyone else finishes by Wednesday night.

### Step 1: Accounts
- A GitHub account: https://github.com/signup
- A **personal** Google account (Gmail). UCLA Google accounts cannot sign in to Antigravity.

### Step 2: Tracker
Download the installer for your system from https://physlets.org/tracker (free; Windows, macOS, Linux) and run it.

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

**Checkpoint:** the last line says `10 passed, 37 xfailed` (or similar, with no `failed`). "xfailed" tests are for functions nobody has written yet. Writing them is your job.

### Step 8: Start the AI agent
In your repository folder:
```
agy
```
Choose **Google OAuth**, sign in with your personal Google account in the browser, and paste the code it gives you back into the terminal. Then type:

> Read AGENTS.md and README.md and explain this project to me in five bullet points.

**Checkpoint:** it explains the project. Press Ctrl+C to quit.

If any step fails, ask for help (section 8).

---

## 2. The video (Tuesday, in the lab)

### Record
Slides 6–8 show the setup. In short: the whole 35 mm dish fills a landscape frame, lit evenly from below; a mm ruler lies **beside the dish with its marks at the height of the water** and stays in the frame; focus and exposure locked; Slo-mo at 240 fps; 60 s without touching the phone. Then, with the same settings, film a stopwatch on a second phone for about 10 s (the stopwatch clip).

Write down: time of recording, when the shrimp hatched (ask the TA), water depth, temperature, the dish's inner diameter.

### Get the original file off the phone
Slo-mo mode records real 240 fps frames, and the original file on the phone keeps all of them (on a computer the original plays at normal speed: that is expected, it is the 240 fps file). But when a slow-motion video leaves the phone through an app or the share button, the phone usually "bakes in" the slow motion: the TA's own test video arrived as a 30 fps file whose first and last seconds play at normal speed and whose middle is slowed down 8 times. Every speed and frequency computed from such a file is wrong. So:

**Never upload a video from the phone's app (Drive, Messages, email, etc.). Copy the original to a computer first.**

- **iPhone:** first, Settings → Photos (or Settings → Apps → Photos) → **Transfer to Mac or PC** → **Keep Originals**. Then either:
  - Windows: connect with a cable, unlock the phone and tap **Trust**, open File Explorer → This PC → Apple iPhone → Internal Storage → DCIM, and copy the `.MOV` file; or
  - Mac: AirDrop the video, but first tap **Options** at the top of the share sheet and turn on **All Photos Data**; or
  - any computer: iCloud.com → Photos → select the video → Download → **Unmodified Originals**.
- **Android:** connect with a cable, choose "File transfer" on the phone, open DCIM → Camera and copy the video file.

Name the files with your group letter, the date and time, and what they are, e.g. `groupB_2026-09-29_1325_main.MOV` and `groupB_2026-09-29_1331_stopwatch.MOV`.

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
Each writes a `..._tracker.mp4` next to the original (a minute of video takes a few minutes). The copy is H.264 with every frame kept, in order, and the phone's rotation applied; it checks that the frame count and frame rate match the original. It is not re-timed: frame n of the copy is frame n of the original.

### Upload
Upload the originals and the `_tracker.mp4` copies to your group's folder in the shared Google Drive (link on slide 10). Videos never go into git (GitHub rejects files over 100 MB, and `.gitignore` refuses them).

---

## 3. Tracking in Tracker (Tuesday → Thursday 1 pm)

The goal: about **10 shrimp, 60 s each, every frame**, one Tracker point mass per shrimp, each exported to its own file. Split the shrimp: 2–3 per person. Positions must be in **mm**, with the **origin at the center of the dish**, x to the right and **y up** (Tracker's default).

### Once per group: calibrate and share (one person, Tuesday)
1. **Open** `..._main_tracker.mp4` in Tracker (File → Open File). Not the `.MOV`: Tracker cannot read it.
2. **fps_true**: open `..._stopwatch_tracker.mp4` in a second tab. Find two frames far apart (e.g. 10 s apart) and note each frame number (shown under the video) and the stopwatch reading. Then fps_true = (frame_b − frame_a) / (time_b − time_a). Your phone says 240; measure it anyway.
3. **Clip Settings** (film-strip button on the toolbar), in the main video's tab: frame rate = fps_true, step size 1.
4. **Calibration**: Calibration button → New → Calibration Stick. Shift-click two ruler marks far apart (e.g. 0 and 30 mm), click the stick's length and type the distance in **mm** (`30`, not `0.03`).
5. **Origin at the dish center**: measuring tools button (ruler icon) → Circle Fitter. Shift-click 4 or more points spread around the inner edge of the dish, then in the circle fitter's menu choose **Move Origin to Center**. Show the axes (Axes button): x to the right and y up (leave Tracker's default).
6. **Check the scale**: measuring tools → Tape Measure on two other ruler marks (e.g. 5 and 25 mm): it must read 20.0 mm within 1%. If not, redo the calibration stick.
7. **Pick the shrimp**: at the first frame, choose about 10 shrimp spread over the dish. Take a screenshot and write a letter next to each (A, B, C, ...). This is the group's map.
8. **Save** (File → Save Tab As) as `groupB_2026-09-29_1325_main.trk` in the same folder as the video, and upload the `.trk` and the map to your group's Drive folder. Everyone opens this `.trk` (keep it next to the video), so the whole group has the same calibration.

### Everyone: autotrack your shrimp
1. Open the group's `.trk`. **Create** (toolbar) → **Point Mass**. Rename it with your shrimp's letter from the map: Track menu → the point mass → Name... → `A`.
2. Turn off **Auto-refresh** (Refresh button on the toolbar → uncheck Auto-refresh): autotracking is much faster.
3. Open the **Autotracker** (toolbar button). Go to the first frame. **Shift+Ctrl+click** the shrimp (Mac: Shift+Cmd+click): this is the key frame. Make the template a small box around the body, and the search area a little larger than one frame's move.
4. Click **Search**. It marks the shrimp frame after frame.
5. It stops when the match is weak (usually two shrimp touching, or the wall). If the mark is on your shrimp, **Accept**. If not, shift-click your shrimp to mark it by hand. **Skip** leaves one frame unmarked.
6. **Not sure which shrimp is yours?** Go back to the last frame you are sure of and use Delete → Later Points: the point mass ends there. If you can pick the same shrimp up again with certainty, continue in a new point mass named `A2` (then `A3`, ...). Never guess: a track that jumps to another shrimp ruins its speed (slide 24).
7. **Check**: play the track back, and look at the x and y plots: a spike is a jump. Delete wrong marks the same way.

Time yourself on the first 10 s (2,400 frames) and post the time on Discord: it tells the TA whether the plan fits.

### Export: one point mass per file
File → Export → Data:
- **Data Table**: choose **one** point mass (e.g. `A`);
- **Columns**: `frame`, `x`, `y` (Tracker always adds `t` first);
- **Cells**: All Cells; **Number Format**: Full Precision; **Delimiter**: comma.

Save it as `A.csv` (the file name is the track's name: `A2.csv`, `B.csv`, ...). Put your files in the `tracks` folder in your group's Drive folder. On Thursday, Role A adds them all to the repository (see below).

### The extras (one person each)
- `extra/still.csv`: autotrack a cyst or speck stuck to the bottom of the dish for 5 s (1,200 frames) and export it the same way. Its apparent motion is your tracking noise σ (slide 29).
- `extra/A_manual.csv`: shrimp A marked **by hand** in frames 400–599: a new point mass, shift-click the shrimp's center in each frame (Tracker moves to the next frame after each click; if it does not, turn on Autostep in the point mass's menu). Exported the same way. Comparing it with the autotracked `A` measures the tracking error (slide 30).
- `extra/body_lengths.csv`: Tracker's tape measure (measuring tools button → Tape Measure), head to tail, on 10 shrimp in frames where each is straight. Type the results into a file with the columns `track_id,frame,length_mm`.

### Where the files go
In the repository, one folder per video, named like the video without its extension:
```
data/tracks/groupB_2026-09-29_1325_main/
    A.csv  A2.csv  B.csv  ...        one file per point mass
    groupB_2026-09-29_1325_main.trk  the group's Tracker file (calibration, all point masses)
    extra/still.csv  extra/A_manual.csv  extra/body_lengths.csv
```
`load_tracks` reads every `.csv` or `.txt` file directly in that folder as a track, so keep other files in `extra/`.

**Before Thursday 1 pm:** every shrimp on the map tracked, played back and exported; the extras done; everything in the group's Drive `tracks` folder.

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

**Adding the Tracker files** (Role A, Thursday): copy the group's `tracks` folder from Drive into `data/tracks/<video name>/` (layout in section 3), then `git add data/tracks` and open a pull request as above. Nobody edits these files afterwards: they are your measurements. To redo a track, export it again from Tracker.

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

## 6. Roles

| Role | Files | Job |
|---|---|---|
| A. Import & calibration | `src/shrimp/load.py` | fps_true from the stopwatch, the manifest, reading Tracker's files into one clean table (mm, real time) with checks that catch a wrong frame rate or scale; adds the Tracker files to the repository |
| B. Kinematics | `src/shrimp/kinematics.py` | speed along a track, smoothing, the tracking noise, jumps (steps no shrimp can make) |
| C. Strokes & Reynolds | `src/shrimp/strokes.py` | stroke frequency, one summary row per track, Reynolds number |
| D. Validation & report | `src/shrimp/synthetic.py`, `validate.py`, `report.py` | synthetic tracks with known physics, the same shrimp tracked twice, every number and figure for the report |

Order on Thursday: A's `read_tracker_csv` and B's `compute_speed` first; C's `summarize_tracks` uses `compute_speed`; D's `report.py` uses everyone's functions. Until those exist, work with `data/example/` (tracks with known physics, see `data/example/README.md`).

Groups of 3: one person does A and B. Groups of 5: split D into validation (`synthetic.py`, `validate.py`) and report (`report.py`). The tables passed between roles are defined in `src/shrimp/formats.py`; change them only if the whole group agrees. `src/shrimp/video.py` and `convert.py` are provided and tested: use them, do not change them.

### Running the analysis
When every role's functions pass their tests:
```
uv run python -m shrimp.report example
uv run python -m shrimp.report groupB_2026-09-29_1325_main.MOV
```
The first runs on `data/example/`, whose answer you know. The second needs your video's row in `data/manifest.csv` (for fps_true) and your files in `data/tracks/groupB_2026-09-29_1325_main/`. It prints one row per track and the numbers for your report, and saves the figures in `results/figures/`.

---

## 7. What to hand in (due Monday Oct 5)

On the `main` branch of your group's repository:
1. Your Tracker files in `data/tracks/<video name>/` (section 3), and your video's row in `data/manifest.csv`.
2. All functions for your roles written, `uv run pytest` passing with no `xfailed` left, and the green check on GitHub.
3. `results/REPORT.md` filled in (template provided), with figures in `results/figures/`:
   - validation: synthetic tracks (the known speed and stroke frequency recovered); shrimp A autotracked vs. marked by hand (RMS difference and bias); the tracking noise σ of a still object, and the speed noise it predicts;
   - physics: speed distribution (histogram, mean ± SD, per frame and per track), stroke frequency (with its resolution), body length (mean ± SD), Reynolds number.
4. Each member authored at least one merged pull request and reviewed at least one.

---

## 8. Asking for help

Discord or email the TA (the links are on slide 4 of the lab slides). Always include:
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
- **`read_tracker_csv` says the file holds several point masses**: export one point mass per file.
- **Numbers in your files use commas for decimals (`1,52`)**: your computer's region settings leaked into the export. Choose a different delimiter than the comma and ask the TA.
- **The agent says you reached a limit**: see section 5.
