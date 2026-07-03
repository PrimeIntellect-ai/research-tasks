You are an AI assistant helping a DevOps team audit historical configuration changes across their server fleet. 

We have a large log file at `/home/user/config_stream.log` representing automated deployment logs. The file contains hundreds of thousands of raw text entries. We need to track the history of two specific configuration parameters: `max_connections` and `timeout`.

Your task is to write a Python script that processes this log file and generates a structured report. 

Requirements:
1. **Large-file Streaming**: The log file is large; process it line-by-line in Python without loading the entire file into memory at once.
2. **Structured Information Extraction**: Each log line looks like this:
   `[2024-01-05 14:32:11] [srv-web-01] [INFO] deploy_bot: "Updated config. max_connections=250, timeout=1m"`
   Extract the date, server name, `max_connections`, and `timeout`. Ignore lines that do not contain these configuration updates.
3. **Normalization**: The `timeout` values in the logs are messy. They might be in seconds (e.g., `30s`, `120s`) or minutes (e.g., `1m`, `2m`). Normalize all timeout values to integer seconds (e.g., `1m` becomes `60`, `120s` becomes `120`).
4. **Resampling and Gap-Filling**: Reconstruct the daily configuration state for three specific servers: `srv-web-01`, `srv-web-02`, and `srv-web-03` for the entire month of January 2024 (2024-01-01 to 2024-01-31). 
   - Assume the baseline state on `2023-12-31` for all servers is `max_connections=100` and `timeout=30`.
   - The state on any given day is the state *at the end of that day* (23:59:59). If multiple changes happen on the same day, use the last one.
   - If no changes occur on a day, forward-fill the configuration state from the previous day.
5. **Anomaly Detection**: Identify any day where a server's `max_connections` increased by **more than 50%** compared to the previous day's end-of-day value.

Output Format:
Create a JSON file at `/home/user/config_report.json` exactly following this structure:
```json
{
  "srv-web-01": {
    "daily_state": {
      "2024-01-01": {"max_connections": 100, "timeout": 30},
      ...
      "2024-01-31": {"max_connections": 250, "timeout": 60}
    },
    "anomalies": ["2024-01-05", "2024-01-18"]
  },
  "srv-web-02": { ... },
  "srv-web-03": { ... }
}
```

Constraints:
- You must use Python. Standard library modules are preferred, but you can install `pandas` or `dateutil` via pip if needed.
- Write and execute your script to produce the final `/home/user/config_report.json` file.