# Data

Videos are NOT stored here. They live in your group's folder in the shared Google Drive.
Git refuses them anyway (see `.gitignore`), and GitHub rejects files over 100 MB.

## File names
Use the date and time of recording, your group letter, and what the clip is:

    groupA_2026-09-29_1325_main.MOV
    groupA_2026-09-29_1331_ruler.MOV
    groupA_2026-09-29_1333_stopwatch.MOV

## data/manifest.csv
One row per main video. Columns:

| column | meaning |
|---|---|
| video_file | file name of the main video |
| drive_link | Google Drive link to it |
| group | your group letter |
| recorded_at | date and time of recording, e.g. 2026-09-29 13:25 |
| hatched_at | when the shrimp hatched (ask the TA), same format |
| phone | phone model |
| slowmo_fps_setting | what the camera app said, e.g. 240 |
| fps_true | frames per second measured from the stopwatch clip |
| um_per_px | micrometres per pixel measured from the ruler clip |
| dish_mm | inner diameter of the dish |
| water_mm | water depth |
| temp_C | water or room temperature |
| notes | anything unusual (bumped the phone, light changed, ...) |
