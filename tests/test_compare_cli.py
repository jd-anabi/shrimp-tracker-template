"""Tests for the provided command line of shrimp.compare: where the figures go. These must always pass.

The students' functions are replaced by stand-ins here, so only the provided part is tested.
"""

from pathlib import Path

import pandas as pd

from shrimp import compare

VIDEO = Path("data") / "tracks" / "groupB_2026-09-29_1325_main"


def test_figures_go_to_the_students_folder():
    assert compare.figures_dir(VIDEO / "ana") == Path("results/ana/figures")
    assert compare.figures_dir(VIDEO / "ana" / "edgetam") == Path("results/ana/figures")
    assert compare.figures_dir(Path("data/example")) == Path("results/figures")
    assert compare.figures_dir(VIDEO) == Path("results/figures")
    assert compare.figures_dir(VIDEO / "edgetam") == Path("results/figures")


def test_tool_name():
    assert compare.tool_name(VIDEO / "ana") == "tracker"
    assert compare.tool_name(VIDEO / "ana" / "edgetam") == "edgetam"
    assert compare.tool_name(VIDEO / "ana" / "sam2") == "sam2"


def test_tools_figure_lands_in_the_students_folder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (VIDEO / "ana").mkdir(parents=True)
    (VIDEO / "ana" / "A.csv").write_text("stand-in\n")
    saved = []
    monkeypatch.setattr(compare, "_one_track", lambda path, fps, name: pd.DataFrame(
        {"track_id": name, "frame": [0, 2], "t_s": [0.0, 2 / fps], "x_mm": [0.0, 0.1], "y_mm": [0.0, 0.0]}))
    monkeypatch.setattr(compare, "tool_comparison", lambda tracks, window_frames=5: pd.DataFrame({"n": [2]}))
    monkeypatch.setattr(compare, "tool_figure", lambda tracks, path: saved.append(Path(path)) or path)
    assert compare.main(["tools", str(VIDEO / "ana"), "A", "--fps", "240"]) == 0
    assert saved == [Path("results/ana/figures/tools_A.png")]


def test_ages_figure_is_named_after_the_tool(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    saved = []
    table = pd.DataFrame({"shrimp": ["A"], "mean_speed_mm_s": [5.0]})
    monkeypatch.setattr(compare, "_per_shrimp", lambda folder, fps: table)
    monkeypatch.setattr(compare, "age_comparison", lambda a, b: pd.DataFrame({"p": [0.5]}))
    monkeypatch.setattr(compare, "age_figure", lambda a, b, path: saved.append(Path(path)) or path)
    day3 = Path("data/tracks/groupB_2026-10-01_1330_main/ana")
    assert compare.main(["ages", str(VIDEO / "ana" / "edgetam"), str(day3 / "edgetam"), "--fps", "240", "240"]) == 0
    assert saved == [Path("results/ana/figures/ages_edgetam.png")]
    assert "WARNING" not in capsys.readouterr().out
    compare.main(["ages", str(VIDEO / "ana" / "edgetam"), str(day3), "--fps", "240", "240"])
    assert "same tool for both ages" in capsys.readouterr().out
