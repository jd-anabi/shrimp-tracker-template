"""Role D: the numbers and figures for REPORT.md, from one video's Tracker files.

Tests: tests/test_report.py. They pass only once every role's functions are written:
analyze_video uses load (A), kinematics (B) and strokes (C).

Usage (from the repository folder), once everything is written:
    uv run python -m shrimp.report groupB_2026-09-29_1325_main.MOV
    uv run python -m shrimp.report example        (the example data in data/example/)
The first reads fps_true for that video from data/manifest.csv and the tracks from
data/tracks/groupB_2026-09-29_1325_main/.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


def analyze_video(folder, fps_true: float, window_frames: int = 9, max_speed_mm_s: float = 100.0,
                  min_duration_s: float = 1.0) -> dict:
    """Everything in section 5 of REPORT.md for one video.

    Steps: load.load_tracks(folder, fps_true) -> kinematics.split_at_jumps(max_speed_mm_s)
    -> strokes.summarize_tracks(window_frames, min_duration_s) and
    kinematics.per_frame_speeds(window_frames). If folder/extra/still.csv exists (a still
    object tracked in Tracker), its tracking noise comes from kinematics.position_noise_mm.

    Returns a dict with at least:
        n_files                 number of point-mass files read
        n_tracks                number of tracks after splitting and dropping short ones
        tracks                  the tracks after splitting (TRACK_COLUMNS)
        summary                 the summarize_tracks table
        frame_speeds_mm_s       the pooled per-frame speeds (numpy array)
        track_speed_mean_mm_s, track_speed_sd_mm_s   mean and SD over tracks of mean_speed_mm_s
        frame_speed_mean_mm_s, frame_speed_sd_mm_s   mean and SD of the per-frame speeds
        stroke_hz_mean, stroke_hz_sd                 mean and SD over tracks of stroke_hz
        noise_mm                position noise from extra/still.csv (NaN if there is none)
    """
    raise NotImplementedError


def make_figures(result: dict, outdir="results/figures", prefix: str = "") -> list:
    """Save the report's figures as PNG files in outdir and return their paths.

    At least: <prefix>speed_histogram.png (per-frame speeds, with the per-track means marked)
    and <prefix>tracks.png (every track's path, x_mm vs y_mm, equal axes, with the dish edge).
    Create outdir if it does not exist. Use matplotlib; label every axis with its unit.
    """
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """PROVIDED: print every number for REPORT.md for one video and save its figures."""
    import numpy as np

    from shrimp import load, strokes, validate  # imported here so `import shrimp.report` works before they exist

    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print(__doc__)
        return 2
    if args[0] == "example":
        folder, fps_true, stem = Path("data/example"), 240.0, "example"
    else:
        manifest = load.load_manifest("data/manifest.csv")
        row = manifest[manifest["video_file"] == args[0]]
        if len(row) != 1:
            print(f"{args[0]} is not in data/manifest.csv (check the spelling, including .MOV)")
            return 1
        stem = Path(args[0]).stem
        folder, fps_true = Path("data/tracks") / stem, float(row["fps_true"].iloc[0])
    window = 9
    result = analyze_video(folder, fps_true, window_frames=window)
    print(f"{folder}: {result['n_files']} files -> {result['n_tracks']} tracks of at least 1 s")
    with pd.option_context("display.width", 120, "display.max_rows", 200):
        print(result["summary"].round(3).to_string(index=False))
    print(f"speed per track:  {result['track_speed_mean_mm_s']:.2f} +/- {result['track_speed_sd_mm_s']:.2f} mm/s (mean +/- SD over tracks)")
    print(f"speed per frame:  {result['frame_speed_mean_mm_s']:.2f} +/- {result['frame_speed_sd_mm_s']:.2f} mm/s (mean +/- SD, w = {window})")
    print(f"stroke frequency: {result['stroke_hz_mean']:.2f} +/- {result['stroke_hz_sd']:.2f} Hz (mean +/- SD over tracks)")
    sigma = result["noise_mm"]
    if np.isfinite(sigma):
        predicted = np.sqrt(2) * sigma / ((window - 1) / fps_true)
        print(f"tracking noise (extra/still.csv): sigma = {sigma * 1000:.1f} um -> speed noise "
              f"sqrt(2) sigma / ((w - 1) dt) = {predicted:.2f} mm/s at w = {window}")
    for manual in sorted((folder / "extra").glob("*_manual.csv")):
        tid = manual.stem[: -len("_manual")]
        raw = load.read_tracker_csv(manual)
        by_hand = pd.DataFrame({"frame": raw["frame"], "t_s": raw["frame"] / fps_true, "x_mm": raw["x"], "y_mm": raw["y"]})
        tracks = result["tracks"]
        auto = tracks[(tracks["track_id"] == tid) | tracks["track_id"].str.startswith(tid + ".")]
        c = validate.compare_tracks(auto, by_hand)
        print(f"{tid}: autotracker vs. by hand, {c['n_frames']} frames: RMS difference {c['rms_difference_mm'] * 1000:.0f} um, "
              f"bias {c['bias_mm'] * 1000:.0f} um, largest {c['max_difference_mm'] * 1000:.0f} um")
    lengths_file = folder / "extra" / "body_lengths.csv"
    if lengths_file.exists():
        lengths = pd.read_csv(lengths_file)["length_mm"]
        re = strokes.reynolds_number(result["track_speed_mean_mm_s"] / 1000, lengths.mean() / 1000)
        print(f"body length: {lengths.mean():.3f} +/- {lengths.std():.3f} mm (mean +/- SD, n = {len(lengths)})")
        print(f"Reynolds number with the mean speed per track and the mean length: Re = {re:.2f}")
    Path("results").mkdir(exist_ok=True)
    out = Path("results") / f"{stem}_tracks_summary.csv"
    result["summary"].to_csv(out, index=False)
    print(f"saved {out}")
    for p in make_figures(result, "results/figures", prefix=f"{stem}_"):
        print(f"saved {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
