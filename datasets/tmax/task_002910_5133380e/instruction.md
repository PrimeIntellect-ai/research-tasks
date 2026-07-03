You are a data scientist tasked with cleaning a multimodal dataset. Our autonomous drone recorded a video feed alongside a stream of tokenized telemetry logs. However, the telemetry sensor experienced intermittent electrical faults, resulting in corrupted ("evil") logs mixed with valid ("clean") logs. 

You must build a C++ log filter that correlates the video visual data with the telemetry logs to detect and reject anomalies.

**Step 1: Video Feature Engineering**
The drone's camera feed is located at `/app/video/sensor_feed.mp4`. 
1. Use `ffmpeg` to extract the frames from this video at exactly 1 frame per second (fps). 
2. Write a script to calculate the mean grayscale pixel intensity (0-255) for each extracted frame.
3. Save these numerical features to `/home/user/frame_brightness.csv` with the exact CSV format: `frame_id,intensity` (e.g., `1,120.5` for the first second/frame, `2,45.2`, etc., up to the end of the video).

**Step 2: Missing Value & Outlier Rule Definition**
Telemetry logs are provided as space-separated tokens. A single log file contains one line like:
`FRAME_005 TEMP_65.2 VOLT_12.1 STAT_OK`
Where `FRAME_005` corresponds to frame_id 5.

A log file is considered **EVIL** (corrupted) if ANY of the following are true:
- Missing Data: Contains any token with `NA` (e.g., `TEMP_NA` or `VOLT_NA`).
- Structural Outlier: The `VOLT_` value is strictly less than `0.0` or strictly greater than `24.0`.
- Contextual (Bayesian Prior) Anomaly: We model the expected temperature based on visual brightness. The expected temperature is `0.75 * intensity`. If the logged `TEMP_` value deviates from this expected temperature by more than `25.0` units (absolute difference), it is anomalous. (If the `FRAME_` ID does not exist in your CSV, treat it as an anomaly).

Otherwise, the log is **CLEAN**.

**Step 3: C++ Detector Implementation**
Write a C++ program at `/home/user/detector.cpp` and compile it to `/home/user/detector` (ensure it is executable).
Your program must accept exactly two command-line arguments:
1. The path to a single telemetry log file.
2. The path to your `frame_brightness.csv` file.

Example invocation:
`/home/user/detector /app/sample_log.txt /home/user/frame_brightness.csv`

The program must parse the specified log file, parse the brightness CSV into memory for lookups, apply the rules defined in Step 2, and print exactly one word to standard output: either `CLEAN` or `EVIL` (followed by a newline).

Your solution will be tested against a hidden, adversarial corpus of clean and evil logs. The verifier will run your executable on every file in the corpus. You must correctly classify 100% of the clean and evil files to pass.