You are a data engineer building an ETL pipeline for a smart factory. You have two data sources to process, integrate, and summarize.

**Part 1: Video Sensor Processing**
There is a video file located at `/app/factory_lights.mp4`. This video records an indicator panel running at exactly 10 frames per second. The video resolution is 300x100 pixels.
- The left region (x: 0-99) tracks the RED sensor.
- The middle region (x: 100-199) tracks the GREEN sensor.
- The right region (x: 200-299) tracks the BLUE sensor.

Your goal is to extract the sensor states for every second of the video (1 second = 10 frames). 
For each 1-second interval (frames 0-9, 10-19, etc.), calculate the mean pixel intensity of the corresponding color channel (Red channel for the left region, Green for the middle, Blue for the right) across all frames in that interval. 
If the mean intensity over the 1-second interval is strictly greater than 100.0, the sensor is considered "ON" (1), otherwise "OFF" (0).

Convert this data into a "long" format CSV named `/home/user/video_data_long.csv` with columns: `second_offset` (integer, starting at 0), `sensor_name` ("red", "green", or "blue"), and `state` (1 or 0). Sort by `second_offset` then `sensor_name`.

**Part 2: Adversarial Log Validation**
You also receive sensor logs in JSON format. Some files are corrupted or contain malicious injections. 
Write a Python script `/home/user/validator.py` that takes a single command-line argument (a directory path) and evaluates every `.json` file inside it. For each file, print exactly one line to `stdout`: either `ACCEPT: filename.json` or `REJECT: filename.json`.

Validation Rules for ACCEPT:
1. The JSON must parse correctly and contain exactly the keys: `timestamp`, `temp`, `pressure`.
2. `temp` must be a numeric value (int or float) between 0.0 and 150.0 (inclusive).
3. `pressure` must be a numeric value between 10.0 and 20.0 (inclusive).
4. `timestamp` must be a string exactly matching the format `YYYY-MM-DDTHH:MM:SSZ` (ISO8601 UTC).

We will run your script against a hidden suite of clean and evil JSON files to verify its accuracy.

**Part 3: Integration & Reporting**
Assume the start of the video (`second_offset = 0`) corresponds to the timestamp `2024-01-01T12:00:00Z`.
Create a final text report at `/home/user/report.txt` summarizing the data using this exact template (replace bracketed values):

```
FACTORY ETL REPORT
Total seconds recorded: [X]
Red sensor ON duration: [Y] seconds
Green sensor ON duration: [Z] seconds
Blue sensor ON duration: [W] seconds
```