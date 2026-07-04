You have just inherited the "AeroSense" IoT backend codebase after the previous developer left abruptly following a severe system crash. You need to investigate the crash by analyzing disparate log files and recovering data from the SQLite database to find a statistical anomaly.

The system state has been prepared in `/home/user/`.
1. **Logs**: There are three log files in `/home/user/logs/`:
   - `gateway.log`: Timestamps are in UNIX Epoch format.
   - `aggregator.log`: Timestamps are in strict ISO8601 format (e.g., `2023-10-25T14:30:00Z`).
   - `db_writer.log`: Timestamps use a custom format `YYYY/MM/DD HH:MM:SS`.
   
   A fatal crash occurred. You need to reconstruct a unified timeline. Parse all three logs, convert their timestamps to standard ISO8601 UTC format (`YYYY-MM-DDTHH:MM:SSZ`), and sort all log entries chronologically. Save this unified log to `/home/user/unified_logs.txt` (format: `[ISO8601_TIMESTAMP] [SOURCE_FILE] MESSAGE`).

2. **Database & Statistical Anomaly**: The SQLite database `/home/user/data/sensors.db` contains a `readings` table (`id INTEGER, sensor_id TEXT, timestamp REAL, value REAL`). Calculate the standard deviation of the `value` column for each `sensor_id`. One sensor went completely rogue right before the crash, exhibiting a drastically higher standard deviation than the others.

3. **Validation Report**: Write a Python script `/home/user/investigate.py` that performs this analysis and generates a final report at `/home/user/report.json`. The JSON file must contain exactly these keys:
   - `"crash_time"`: The ISO8601 timestamp of the log entry containing the word "FATAL" (string).
   - `"anomalous_sensor"`: The `sensor_id` with the highest standard deviation in its readings (string).
   - `"highest_stddev"`: The standard deviation of that anomalous sensor, rounded to 2 decimal places (float).

You may install any required Python packages (like `pandas` or `numpy`), though the standard library (`sqlite3`, `datetime`, `statistics`, `json`) is sufficient.