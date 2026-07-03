You are a log analyst investigating a recent system anomaly. We have captured an audio dictation from the on-call engineer that describes the specific subsystem they suspect is failing. We also have a massive dump of our raw telemetry data.

Your objectives:

1. Transcribe or listen to `/app/incident_report.wav` to identify the specific metric prefix we need to investigate (e.g., `cpu_`, `mem_`, etc.). You may use any available terminal tools or install necessary libraries (e.g., Python `SpeechRecognition` or `whisper`) to extract this information.
2. Read the raw telemetry logs located at `/app/telemetry.jsonl`. This is a large file, so you must process it using a streaming approach in **Go**.
3. The JSON-lines file has a known corruption issue: a buggy logging agent injected invalid unicode escape sequences (e.g., `\uXYZW`) into the `message` field of some lines, which breaks standard JSON parsers. Your Go program must elegantly recover from or sanitize these errors while parsing.
4. The logs contain a wide-format `metrics` object (e.g., `{"ts": 1700000000, "host": "web-01", "metrics": {"net_rx": 50, "disk_io_read": 12, ...}, "message": "..."}`). You must reshape this into a long format for the target metrics identified in the audio file.
5. Compute a 5-minute (300 seconds) rolling average of the target metrics, grouped by `host` and `metric_name`. The rolling window should be evaluated at every new timestamp present in the logs for that host/metric. 
6. Output the results to `/home/user/aggregated_metrics.csv` with the exact header: `window_end_ts,host,metric_name,rolling_avg`.

Requirements:
- Your primary data processing pipeline MUST be written in Go.
- Do not load the entire JSON file into memory; use a streaming reader.
- The output CSV must be sorted chronologically by `window_end_ts`, then by `host`, then by `metric_name`.

Our automated test suite will evaluate your CSV against our ground-truth data using a Mean Squared Error (MSE) metric to verify your rolling aggregation math.