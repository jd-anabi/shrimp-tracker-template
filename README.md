# Brine shrimp tracker (Physics M180G, Fall 2026)

Your group builds a program that finds every brine shrimp in a slow-motion video, follows each one over time, and measures how they swim. You write the code with an AI agent (Antigravity CLI); you are responsible for checking that it is right.

- Slides for this lab: shared by the TA
- Questions: Discord >>> PASTE DISCORD LINK HERE <<< or email the TA
- Videos: shared Google Drive folder >>> PASTE GOOGLE DRIVE FOLDER LINK HERE <<<

Contents: [1. Setup](#1-one-time-setup-due-wednesday-night) · [2. Original videos](#2-getting-the-original-video-off-your-phone) · [3. Daily workflow](#3-how-we-work-every-time) · [4. The agent](#4-working-with-the-agent) · [5. Roles](#5-roles) · [6. What to hand in](#6-what-to-hand-in-due-monday-oct-5) · [7. Help](#7-asking-for-help) · [8. Troubleshooting](#8-troubleshooting)

---

## 1. One-time setup (due Wednesday night)

You need a laptop with Windows, macOS or Linux. Chromebooks and iPads will not work; tell the TA by Monday if that is all you have. Each step ends with a **checkpoint**: do not continue until it works.

### Step 1: Accounts
- A GitHub account: https://github.com/signup
- A **personal** Google account (Gmail). UCLA Google accounts cannot sign in to Antigravity.

### Step 2: Open a terminal
- Windows: Start menu, type `PowerShell`, open **Windows PowerShell**.
- macOS: press Cmd+Space, type `Terminal`, press Enter.
- Linux: open your Terminal app.

Type each command below into the terminal and press Enter. Paths with spaces need quotes: `cd "My Folder"`.

### Step 3: Install the tools

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

### Step 4: Connect the terminal to GitHub
```
gh auth login
```
Choose: **GitHub.com** → **HTTPS** → **Yes** (authenticate Git) → **Login with a web browser**. Copy the one-time code, press Enter, paste the code in the browser.

**Checkpoint:** `gh auth status` says you are logged in.

### Step 5: Get your group's repository
One person per group, once:
1. Open the template: >>> PASTE TEMPLATE REPO LINK HERE <<<
2. Click **Use this template** → **Create a new repository**. Owner: you. Name: `shrimp-group-<letter>`. Choose **Private**. Create.
3. In the new repository: **Settings** → **Collaborators** → add your teammates and the TA (>>> PASTE TA GITHUB USERNAME HERE <<<).

Everyone (after accepting the invitation email):
```
cd Documents
gh repo clone <owner>/shrimp-group-<letter>
cd shrimp-group-<letter>
```

**Checkpoint:** `git status` says `On branch main`.

### Step 6: Install the Python packages and run the tests
```
uv sync
uv run pytest
```
The first `uv sync` downloads Python and the packages; it can take a few minutes.

**Checkpoint:** the last line says `8 passed, 24 xfailed` (or similar, with no `failed`). "xfailed" tests are for functions nobody has written yet. Writing them is your job.

### Step 7: Start the AI agent
In your repository folder:
```
agy
```
Choose **Google OAuth**, sign in with your personal Google account in the browser, and paste the code it gives you back into the terminal. Then type:

> Read AGENTS.md and README.md and explain this project to me in five bullet points.

**Checkpoint:** it explains the project. Press Ctrl+C to quit.

If any step fails, ask for help (section 7) before Thursday.

---

## 2. Getting the original video off your phone

Slo-mo mode records real 240 fps frames, and the original file on the phone keeps all of them (on a computer the original plays at normal speed: that is expected, it is the 240 fps file). But when a slow-motion video leaves the phone through an app or the share button, the phone usually "bakes in" the slow motion. The TA's own Slo-mo test video arrived as a 30 fps file whose first and last seconds play at normal speed and whose middle is slowed down 8 times. Every speed and frequency computed from such a file is wrong. So:

**Never upload a video from the phone's app (Drive, Messages, email, etc.). Copy the original to a computer first.**

- **iPhone:** first, Settings → Photos (or Settings → Apps → Photos) → **Transfer to Mac or PC** → **Keep Originals**. Then either:
  - Windows: connect with a cable, unlock the phone and tap **Trust**, open File Explorer → This PC → Apple iPhone → Internal Storage → DCIM, and copy the `.MOV` file; or
  - Mac: AirDrop the video, but first tap **Options** at the top of the share sheet and turn on **All Photos Data**; or
  - any computer: iCloud.com → Photos → select the video → Download → **Unmodified Originals**.
- **Android:** connect with a cable, choose "File transfer" on the phone, open DCIM → Camera and copy the video file.

Then check the file (tip: drag the file onto the terminal window to paste its path):
```
uv run python -m shrimp.check_video "path/to/your/video.MOV"
```
It must end with `OK`. If it prints a `WARNING`, do not use the file: post the output on Discord.

Finally upload the original to your group's folder in the shared Google Drive and add a row to `data/manifest.csv` (see `data/README.md`). Videos never go into git.

---

## 3. How we work (every time)

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
git commit -m "Say what you changed, e.g. Detect shrimp by background subtraction"
git push -u origin HEAD
gh pr create --web
```
`gh pr create --web` opens the pull request page in your browser; answer the questions in the description (what you asked the agent, how you checked it). A teammate reviews the pull request on GitHub (**Files changed** → comment → **Approve**), then the author clicks **Merge**. Afterwards everyone runs `git switch main` and `git pull`.

Every pull request must pass the automatic tests (the green check on GitHub).

---

## 4. Working with the agent

The agent reads `AGENTS.md` (the project rules) every time it starts. Your rules:
- Keep it in review mode, where it asks before changing files. Never switch to "always proceed".
- Start each task by asking for a plan. Then ask for tests first, then the code, then `uv run pytest`.
- Read every change before accepting it. You must be able to explain your module in lab.
- Use a Flash model by default (`/model`). Switch to Gemini 3.1 Pro or Claude only for hard problems: the free plan has weekly limits.
- Do not use `/boost` or `/teamwork-preview`; they run several agents at once and use up your limit.
- `/rewind` undoes the agent's last steps. Git undoes everything else.
- If you hit your weekly limit: switch to a Flash model, work with a teammate, and tell the TA.

---

## 5. Roles

| Role | Files | Job |
|---|---|---|
| A. Video & calibration | `src/shrimp/calibrate.py` | true frame rate from the stopwatch clip, µm per pixel from the ruler clip, the manifest |
| B. Detection | `src/shrimp/detect.py` | background image, find every shrimp in every frame |
| C. Tracking | `src/shrimp/track.py` | link detections into one track per shrimp |
| D. Analysis & validation | `src/shrimp/analyze.py`, `synthetic.py`, `validate.py` | synthetic video, scores against the truth, physics results |

Groups of 3: one person does A and B. Groups of 5: split D into validation (`synthetic.py`, `validate.py`) and analysis (`analyze.py`). The tables passed between roles are defined in `src/shrimp/formats.py`; change them only if the whole group agrees. `src/shrimp/video.py` is provided and tested: use it, do not change it.

---

## 6. What to hand in (due Monday Oct 5)

On the `main` branch of your group's repository:
1. All functions for your roles written, `uv run pytest` passing with no `xfailed` left, and the green check on GitHub.
2. `results/REPORT.md` filled in (template provided), with figures in `results/figures/`:
   - validation on the synthetic video: recall, precision, RMS position error, identity switches;
   - validation on your real video: the same scores against about 200 frames of at least 3 shrimp that you tracked by hand;
   - an overlay image or short clip of the tracks drawn on the real video;
   - physics: speed distribution (histogram, mean ± SD), stroke frequency (with its resolution), body length (mean ± SD), Reynolds number.
3. Each member authored at least one merged pull request and reviewed at least one.

---

## 7. Asking for help

Discord (>>> PASTE DISCORD LINK HERE <<<) or email the TA. Always include:
- your operating system,
- the exact command you typed,
- the full error text (copy and paste, not just a photo),
- a screenshot,
- what you already tried.

The TA is in the lab Tuesdays and Thursdays 1–3 pm.

---

## 8. Troubleshooting

- **"not recognized" / "command not found"**: close and reopen the terminal. If it still fails, run the install line again.
- **`winget` not found (Windows)**: install Git from https://git-scm.com/download/win and the GitHub CLI from https://cli.github.com, then continue.
- **"running scripts is disabled" (Windows)**: use the uv install line exactly as written; it includes `-ExecutionPolicy ByPass`.
- **`uv sync` fails**: check your internet connection and run it again; if it still fails, post the full error.
- **`gh repo clone` says not found**: accept the invitation email first, and check the owner and name.
- **`git push` is rejected**: someone merged first. Run `git pull`, then push again. Ask for help if git mentions a conflict.
- **`check_video` prints a WARNING**: you have a re-timed copy. Redo section 2.
- **The agent says you reached a limit**: see section 4.
