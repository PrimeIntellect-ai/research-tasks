As a log analyst investigating a recent data center anomaly, you must correlate physical server rack activity with sparse network logs. We have provided a security camera video of the server rack at `/app/server_cam.mp4` and a fragmented log file at `/home/user/sparse_logs.csv`.

Your task is to build a Go-based data pipeline and investigation service that performs the following steps:

1. **Video Extraction:** Use `ffmpeg` (preinstalled) to process `/app/server_cam.mp4`. Analyze the video to determine the "flash count" per second. A flash is defined as a frame where the average pixel brightness exceeds a threshold of 180 (on a 0-255 grayscale). Assume the video runs at 10 fps.
2. **Resampling and Gap-Filling:** The `/home/user/sparse_logs.csv` file contains UNIX timestamps and an `error_rate` float. However, it is missing entries for several seconds. Read the CSV, resample it to a strict 1-second interval grid matching the video duration (starting from the first timestamp in the CSV), and fill any missing gaps by carrying forward the last known `error_rate`.
3. **Rolling Statistics Computation:** Merge the per-second video flash count with the gap-filled log data. Calculate an `anomaly_score` for each second: `(flash_count * 0.5) + error_rate`. Then, compute a 5-second rolling moving average of this `anomaly_score` for each second (using the current second and the previous 4 seconds; if less than 5 seconds are available, average the available seconds).
4. **Template-Based Text Generation:** Use Go's `text/template` package to generate an `incident_report.txt` file. The template must output: "Maximum Rolling Anomaly Score: [Max Score] at second [Second Offset]".
5. **API Service:** Write a Go HTTP server listening exactly on `0.0.0.0:9090` that serves the following endpoints:
   - `GET /stats`: Returns a JSON array of objects representing the per-second data: `[{"second": 0, "anomaly_score": 1.5, "rolling_avg": 1.5}, ...]`.
   - `GET /report`: Returns the raw plain text of the generated `incident_report.txt`.

Ensure your Go application is fully self-contained, compiles, and runs continuously in the background to serve the API. Do not hardcode the expected outputs; compute them dynamically.