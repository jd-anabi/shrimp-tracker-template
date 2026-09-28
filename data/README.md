# Data

## Videos: never in git
Videos live in your group's folder in the shared Google Drive: the originals (`.MOV`) and
the copies Tracker can open (`_tracker.mp4`, made with `shrimp.convert`). Git refuses them
anyway (see `.gitignore`), and GitHub rejects files over 100 MB. If you want a video on your
laptop inside the repository, put it in `data/raw/` (ignored by git).

File names: your group letter, the date and time of recording, and what the clip is:

    groupB_2026-09-29_1325_main.MOV            the 60 s video of the dish (with the ruler in view)
    groupB_2026-09-29_1325_main_tracker.mp4    its copy for Tracker
    groupB_2026-09-29_1331_stopwatch.MOV       the stopwatch clip

## Tracks: in git
One folder per video in `data/tracks/`, named like the video without its extension:

    data/tracks/groupB_2026-09-29_1325_main/
        A.csv  A2.csv  B.csv  ...           one file per Tracker point mass (= one track)
        groupB_2026-09-29_1325_main.trk     the group's Tracker file
        extra/still.csv                     a still object (a cyst stuck to the dish), autotracked
        extra/A_manual.csv                  shrimp A marked by hand, frames 400-599
        extra/body_lengths.csv              columns track_id,frame,length_mm (tape measure)

Every `.csv` or `.txt` file directly in the video's folder is read as a track, and its file
name (without the extension) is the track's name. Keep anything else in `extra/`. These files
are measurements: nobody edits them. To redo a track, export it again from Tracker.

`data/example/` has the same layout, with synthetic tracks whose physics is known
(see `data/example/README.md`). Use it to develop and check your code.

## data/manifest.csv
One row per main video. Columns:

| column | meaning |
|---|---|
| video_file | file name of the original main video, e.g. groupB_2026-09-29_1325_main.MOV |
| drive_link | Google Drive link to it |
| group | your group letter |
| recorded_at | date and time of recording, e.g. 2026-09-29 13:25 |
| hatched_at | when the shrimp hatched (ask the TA), same format |
| phone | phone model |
| slowmo_fps_setting | what the camera app said, e.g. 240 |
| fps_true | frames per second measured from the stopwatch clip (also typed into Tracker's Clip Settings) |
| stick_mm | length of Tracker's calibration stick on the ruler, in mm |
| check_mm | Tracker's tape measure on a different ruler interval (e.g. 20 mm): the scale check |
| dish_mm | inner diameter of the dish, measured with a ruler |
| water_mm | water depth |
| temp_C | water or room temperature |
| notes | anything unusual (bumped the phone, light changed, ...) |
