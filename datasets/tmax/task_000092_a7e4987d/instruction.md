You need to implement a Configuration Drift Tracker that processes server configuration logs, calculates rolling aggregations, and schedules reports.

We have a legacy system specification stored as an image at `/app/config_spec.png`. This image contains two critical parameters written in plain text:
- `WINDOW_SIZE`: The sliding window duration in seconds.
- `DRIFT_THRESHOLD`: The minimum number of changes required in the window to trigger a report entry.

Your tasks:
1. Extract the `WINDOW_SIZE` and `DRIFT_THRESHOLD` from the image `/app/config_spec.png`. You can use `tesseract-ocr` which is pre-installed.
2. Create a Rust project at `/home/user/drift_monitor`.
3. The Rust program must read `/app/config_logs.csv` (which has columns: `timestamp`, `server_id`, `config_bytes`). The `timestamp` is a Unix epoch integer.
4. For every row in the CSV (processed in chronological order), calculate the rolling average of `config_bytes` over the preceding `WINDOW_SIZE` seconds (inclusive of the current row's timestamp).
5. If the number of logs within that window is strictly greater than `DRIFT_THRESHOLD`, use a template-based string formatting to append a line to `/home/user/drift_report.txt` in the exact format:
   `[TIMESTAMP] Server config drift detected. Rolling average config size: [AVERAGE] bytes.`
   *(Format `AVERAGE` to exactly 2 decimal places).*
6. Set up a cron job for the `user` that runs the compiled Rust release binary every minute. The cron job should execute `/home/user/drift_monitor/target/release/drift_monitor`.

Ensure your calculations are highly accurate. Your output will be evaluated based on the Mean Squared Error (MSE) of the computed rolling averages compared to the reference baseline.