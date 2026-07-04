You are a data engineer tasked with building a robust video telemetry ETL pipeline. We receive raw video footage and structured JSON telemetry streams from remote traffic cameras. 

Your task consists of three parts:

1. **Telemetry Sanitizer:**
Create a Python script at `/home/user/filter_telemetry.py` that reads a JSON file path as its first argument and outputs valid JSON lines to standard out, dropping invalid ones. 
Valid telemetry records must have:
- `timestamp`: float >= 0.0
- `frame_id`: integer >= 0
- `bbox`: exactly 4 integers (all >= 0)
- `confidence`: float between 0.0 and 1.0 inclusive
Any records missing these fields, having incorrect types, or violating these constraints must be silently discarded.

2. **Video ETL Pipeline:**
Create a Python script at `/home/user/process_video.py`. This script must:
- Process the video file located exactly at `/app/traffic.mp4`.
- Extract every frame (assume 30 FPS).
- Calculate the mean grayscale brightness of each frame.
- Sort by `frame_id` and handle potential frame drops by gap-filling missing `frame_id`s (carrying forward the previous frame's brightness).
- Calculate a 5-frame rolling average of the brightness.
- Output the result to `/home/user/video_stats.csv` with columns: `frame_id,timestamp_sec,brightness,rolling_avg`.

3. **Pipeline Scheduling:**
Configure a cron job for the current user that executes `/home/user/process_video.py` exactly at the top of every hour (minute 0).

Ensure all scripts are executable and handle errors gracefully.