"""Role D: compare the three tools on one shrimp, and the two ages over many shrimp.

Tests: tests/test_compare.py. Build each function with your agent (tests first!).
They use other roles' functions: load (A), motion and kinematics (B), strokes and stats (C).

Usage (from the repository folder), once everything is written:
    uv run python -m shrimp.compare tools data/tracks/groupB_2026-09-29_1325_main/ana A
        Shrimp A in Tracker (ana/A.csv), SAM 2 (ana/sam2/A.csv) and EdgeTAM (ana/edgetam/A.csv).
    uv run python -m shrimp.compare ages data/tracks/groupB_2026-09-29_1325_main/ana data/tracks/groupB_2026-10-01_1330_main/ana
        Every shrimp in the first folder (1 day old) against every shrimp in the second (3 days old).
        Use the same tool for both ages (e.g. .../ana/edgetam for both).
    uv run python -m shrimp.compare tools data/example A          (example data, known answers)
    uv run python -m shrimp.compare ages data/example data/example_day3
fps_true comes from data/manifest.csv (the folder's video name) or from --fps.
Figures go to results/<student>/figures/ for a folder in data/tracks/<video>/<student>/ (results/figures/ for
the example data, or --out): tools_<shrimp>.png and ages_<tool>.png, e.g. results/ana/figures/tools_A.png.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

TOOLS = ["tracker", "sam2", "edgetam"]


def tool_comparison(tracks: dict[str, pd.DataFrame], window_frames: int = 5) -> pd.DataFrame:
    """Compare tools on the SAME shrimp. `tracks` = {tool: one track (formats.TRACK_COLUMNS)}; the
    first tool is the reference (Tracker).

    One row per tool (index = tool name) with the columns n_frames, duration_s, mean_speed_mm_s,
    stroke_hz, stroke_period_s (from strokes.summarize_tracks with window_frames, and 1 / stroke_hz),
    rms_difference_mm and bias_mm (validate.compare_tracks against the first tool; 0 for the first).
    """
    raise NotImplementedError


def tool_figure(tracks: dict[str, pd.DataFrame], path) -> Path:
    """Save a figure of the same shrimp seen by each tool and return its path.

    Four panels sharing the time axis (s): x and y (mm), vx and vy (mm/s), ax and ay (mm/s^2),
    speed (mm/s), from motion.velocity_acceleration; one color per tool, with a legend. Create the
    folder if needed. Use matplotlib and save to a file (no plt.show()).
    """
    raise NotImplementedError


def age_comparison(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    """Compare two stats.per_shrimp tables (a: younger, b: older).

    One row per quantity (index: mean_speed_mm_s, stroke_hz, stroke_period_s) with the columns
    n_a, mean_a, sd_a, n_b, mean_b, sd_b (stats.describe) and difference, t, df, p
    (stats.welch_test(a, b)).
    """
    raise NotImplementedError


def age_figure(a: pd.DataFrame, b: pd.DataFrame, path, labels=("1 day old", "3 days old")) -> Path:
    """Save histograms of average speed, stroke frequency and stroke period (one panel each, both ages
    in each panel, labelled with mean +/- SD and n) and return the path. Create the folder if needed."""
    raise NotImplementedError


# ------------------------------------------------------------------ PROVIDED: the command line

def figures_dir(folder: Path) -> Path:
    """Where figures go: results/<student>/figures for data/tracks/<video>/<student>[/<tool>], else
    results/figures (e.g. for the example data)."""
    parts = Path(folder).parts
    if "tracks" in parts:
        i = len(parts) - 1 - parts[::-1].index("tracks")
        if len(parts) > i + 2 and parts[i + 2] not in ("sam2", "sam2-small", "edgetam", "extra"):
            return Path("results") / parts[i + 2] / "figures"
    return Path("results") / "figures"


def tool_name(folder: Path) -> str:
    """The tool a folder of tracks comes from: its sam2/ or edgetam/ subfolder name, otherwise Tracker."""
    last = Path(folder).name
    return last if last in ("sam2", "sam2-small", "edgetam") else "tracker"


def _fps_for(folder: Path, manifest: Path = Path("data/manifest.csv")) -> float | None:
    """fps_true of the video a folder belongs to: data/tracks/<video name>/... -> data/manifest.csv."""
    if "example" in folder.parts or any(p.startswith("example") for p in folder.parts):
        return 240.0
    if not manifest.exists():
        return None
    m = pd.read_csv(manifest, dtype=str)
    stems = {Path(v).stem: f for v, f in zip(m.get("video_file", []), m.get("fps_true", []))}
    for part in [folder, *folder.parents]:
        if part.name in stems:
            return float(stems[part.name])
    return None


def _one_track(path: Path, fps: float, name: str) -> pd.DataFrame:
    from shrimp import load

    d = load.read_tracker_csv(path)
    return pd.DataFrame({"track_id": name, "frame": d["frame"], "t_s": d["frame"] / fps, "x_mm": d["x"],
                         "y_mm": d["y"]}).sort_values("frame").reset_index(drop=True)


def _window(tracks: pd.DataFrame) -> int:
    """Rows spanning about 8 frames (33 ms at 240 fps) whatever the step: 9 at step 1, 5 at step 2."""
    step = max(int(tracks.groupby("track_id")["frame"].diff().median()), 1)
    return 2 * max(1, round(4 / step)) + 1


def _per_shrimp(folder: Path, fps: float):
    from shrimp import kinematics, load, stats, strokes

    tracks = kinematics.split_at_jumps(load.load_tracks(folder, fps))
    return stats.per_shrimp(strokes.summarize_tracks(tracks, window_frames=_window(tracks)))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m shrimp.compare", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="what", required=True)
    t = sub.add_parser("tools", help="one shrimp, three tools")
    t.add_argument("folder")
    t.add_argument("name")
    t.add_argument("--fps", type=float)
    t.add_argument("--out", help="folder for the figure (default: results/<student>/figures)")
    g = sub.add_parser("ages", help="many shrimp, two ages")
    g.add_argument("folder_young")
    g.add_argument("folder_old")
    g.add_argument("--fps", type=float, nargs=2, metavar=("FPS_YOUNG", "FPS_OLD"))
    g.add_argument("--out", help="folder for the figure (default: results/<student>/figures)")
    a = p.parse_args(sys.argv[1:] if argv is None else argv)
    pd.set_option("display.width", 140)
    if a.what == "tools":
        folder = Path(a.folder)
        fps = a.fps or _fps_for(folder)
        if fps is None:
            print("Unknown fps_true: add the video to data/manifest.csv or give --fps.")
            return 1
        files = {"tracker": folder / f"{a.name}.csv", "sam2": folder / "sam2" / f"{a.name}.csv",
                 "edgetam": folder / "edgetam" / f"{a.name}.csv"}
        tracks = {tool: _one_track(f, fps, tool) for tool, f in files.items() if f.exists()}
        if "tracker" not in tracks:
            print(f"{files['tracker']} not found: export shrimp {a.name} from Tracker into {folder} first.")
            return 1
        table = tool_comparison(tracks, window_frames=_window(pd.concat(tracks.values())))
        print(table.round(4).to_string())
        out = Path(a.out) if a.out else figures_dir(folder)
        name = re.sub(r"[^A-Za-z0-9_.-]+", "_", a.name)
        print(f"saved {tool_figure(tracks, out / f'tools_{name}.png')}")
        return 0
    young, old = Path(a.folder_young), Path(a.folder_old)
    tool = tool_name(young)
    if tool_name(old) != tool:
        print(f"WARNING: {young} holds {tool} tracks but {old} holds {tool_name(old)} tracks. Use the same "
              "tool for both ages: the tools do not follow the same point of the shrimp.")
    fps = a.fps or (_fps_for(young), _fps_for(old))
    if None in fps:
        print("Unknown fps_true: add both videos to data/manifest.csv or give --fps FPS_YOUNG FPS_OLD.")
        return 1
    ya, ob = _per_shrimp(young, fps[0]), _per_shrimp(old, fps[1])
    for label, tab in (("younger", ya), ("older", ob)):
        print(f"{label}: {len(tab)} shrimp")
        print(tab.round(3).to_string(index=False))
    print(age_comparison(ya, ob).round(4).to_string())
    out = Path(a.out) if a.out else figures_dir(young)
    print(f"saved {age_figure(ya, ob, out / f'ages_{tool}.png')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
