You are a log analyst investigating server performance patterns. You have received a raw CSV log file at `/home/user/server_metrics.csv` containing irregular, high-frequency telemetry data from various servers. The file can be conceptually massive, so you must process it efficiently using Python.

The CSV has three columns:
`timestamp` (format: YYYY-MM-DD HH:MM:SS)
`server_id` (string)
`cpu_usage` (float)

Your task is to write and execute a Python script to process this data through an ETL pipeline that cleans, gap-fills, and stratifies the logs:

1. **Filter**: Retain only logs for servers whose `server_id` starts with the prefix `"PROD-"`. Ignore all other servers (e.g., DEV-, TEST-).
2. **Aggregate (Downsample)**: Round down all timestamps to the nearest minute (e.g., `10:01:45` becomes `10:01:00`). If a server has multiple log entries in the same minute, calculate the arithmetic mean of the `cpu_usage` for that minute.
3. **Resample and Gap-fill**: The logs often drop out, leaving gaps of several minutes. For each `PROD-` server independently, create a continuous 1-minute frequency time series from its earliest recorded aggregated minute to its latest recorded aggregated minute. Fill any missing `cpu_usage` values using **linear interpolation**.
4. **Stratified Sampling**: From the continuous, gap-filled time series, extract only the first 5 minutes of every hour (i.e., minutes `00`, `01`, `02`, `03`, and `04`).
5. **Output**: Save the final extracted records to `/home/user/processed_logs.json`. The output must be a JSON array of objects, sorted chronologically by `timestamp`, and then alphabetically by `server_id`. 

The JSON format must strictly be:
```json
[
  {
    "timestamp": "YYYY-MM-DD HH:MM:00",
    "server_id": "PROD-A",
    "cpu_usage": 55.0
  },
  ...
]
```
Ensure that `cpu_usage` is rounded to exactly 2 decimal places in the final JSON. 

Write the Python script, execute it, and ensure `/home/user/processed_logs.json` is created with the correct data.