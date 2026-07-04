You are an automation specialist for an industrial drone monitoring system. You are tasked with building a robust Python data processing pipeline that correlates visual telemetry feeds with external sensor logs. However, the system is currently experiencing a data poisoning attack, meaning some of the external logs contain malicious anomalies.

Your task has three main phases:

**Phase 1: Visual Telemetry Extraction (Parallel Processing & Imputation)**
You are provided with a drone dashcam video at `/app/drone_feed.mp4`. 
1. Use `ffmpeg` and Python to extract the frame-by-frame average grayscale luminance (0-255 scale) of the video. The video runs at exactly 30 fps.
2. Implement a parallel processing approach (e.g., `multiprocessing`) to speed up the frame analysis.
3. Due to transmission errors, some frames in the video are completely black (average luminance exactly 0.0). Treat these as missing data. Apply linear interpolation to impute the luminance values for these missing frames based on the nearest valid frames.
4. Save the interpolated visual telemetry as a CSV at `/home/user/visual_telemetry.csv` with columns: `frame_index`, `timestamp` (in seconds, e.g., 0.000, 0.033, 0.066), and `luminance`.

**Phase 2: Log Sanitization (Adversarial Filtering)**
We are receiving external sensor logs, but some are corrupted or malicious. You must write a robust anomaly detector script.
1. Create a Python script at `/home/user/log_sanitizer.py`.
2. The script must accept a single command-line argument: the path to a CSV log file.
3. The CSV files have columns: `timestamp`, `sensor_reading`.
4. The script must analyze the file and determine if it is "clean" or "evil".
5. It should exit with code `0` if the file is clean, and code `1` if the file is evil.
6. "Evil" files contain one or more of the following anomalies: 
   - Unrealistic jumps: The absolute difference between consecutive `sensor_reading` values strictly exceeds 50.0.
   - Impossible values: Any `sensor_reading` is strictly less than 0.
   - Excessive missing data: More than 5% of the `sensor_reading` values are empty or NaN.
   - Non-numeric injections: Strings that cannot be parsed as floats in the `sensor_reading` column.
7. Clean files will have smooth interpolations, non-negative values, and <= 5% missing data.

**Phase 3: Aggregation and Stratification**
Assume all files that your sanitizer passes are clean. 
1. Read all the clean CSV logs from the directory `/app/sensor_logs/` (skip the evil ones!).
2. Merge these clean logs with your `/home/user/visual_telemetry.csv` using the `timestamp` column (use a tolerance of 0.01 seconds for matching timestamps, performing an outer join to keep all data).
3. Stratify the merged dataset into 5-second tumbling windows (0.0-4.99s, 5.0-9.99s, etc.).
4. For each stratum, compute the summary statistics: the mean of `luminance`, the mean of `sensor_reading`, and the total count of valid (non-null) records for each.
5. Save the final aggregated result to `/home/user/strata_summary.json`. 

The JSON should be formatted exactly like this:
```json
{
  "0": {
    "mean_luminance": 120.5,
    "mean_sensor": 45.2,
    "count_luminance": 150,
    "count_sensor": 140
  },
  "5": { ... }
}
```
(Where "0" represents the 0-4.99s window, "5" represents 5-9.99s, etc. Round means to 2 decimal places).