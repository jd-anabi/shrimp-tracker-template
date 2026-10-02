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
    groupB_2026-10-01_1330_main.MOV            Thursday: the same dish, 3 days old

## Tracks: in git
One folder per video in `data/tracks/`, named like the video without its extension, and in it one
folder per student (first name, lowercase):

    data/tracks/groupB_2026-09-29_1325_main/
        groupB_2026-09-29_1325_main.trk     the group's Tracker file (calibration)
        ana/
            A.csv  A2.csv  B.csv  ...       one file per Tracker point mass (= one track)
            sam2/A.csv  sam2/run.log        written by shrimp.segment (SAM 2)
            edgetam/A.csv  edgetam/B.csv    written by shrimp.segment (EdgeTAM)
            extra/start.csv                 one mark per shrimp on one frame, several point masses
                                            in one file: the input of shrimp.segment for many shrimp

Every `.csv` or `.txt` file directly in a folder is read as a track, and its file name (without
the extension) is the track's name: `A2` is the second piece of shrimp `A`. Keep anything else in
`extra/`. Files written by `shrimp.segment` have the same format as Tracker's, plus empty x and y in
frames where the model lost the shrimp. These files are measurements: nobody edits them. To redo a
track, export it again from Tracker or run the script again. `overlay.mp4` (the video with the
outlines) is written next to them but stays out of git.

`data/example/` (1 day old, with `sam2/` and `edgetam/` versions of shrimp A) and
`data/example_day3/` (3 days old) are laid out like one student's folder, with synthetic tracks whose
physics is known (see their README files). Use them to develop and check your code.

## data/manifest.csv
One row per main video (so two rows per group: 1 and 3 days old). Columns:

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
