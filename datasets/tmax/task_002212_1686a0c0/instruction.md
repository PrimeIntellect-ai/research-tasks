You are an observability engineer tasked with tuning our local dashboard metrics pipeline. An upstream legacy application is continuously dumping highly noisy logs, and our current dashboard backend expects clean, aggregated data.

We need you to build a pipeline that extracts metric data, calculates the 90th percentile (P90) latency per endpoint, and logs the aggregated results with strict rotation policies to prevent disk exhaustion.

Here are your instructions:

**Phase 1: Log Extraction Pipeline**
A noisy log file is located at `/home/user/raw_app.log`. 
Write a shell command or script using text processing tools (like `awk`, `grep`, `sed`) to extract only the log lines that contain the exact tag `[METRIC]`. 
From those lines, parse out the `timestamp`, `endpoint`, `latency` (numeric value only, strip the 'ms'), and `status`.
Write the extracted data as a comma-separated values file to `/home/user/parsed_metrics.csv` with exactly this format (no header row):
`timestamp,endpoint,latency,status`

*Example raw log line:*
`2023-10-01T12:00:01Z [INFO] User logged in successfully` (Ignore this)
`2023-10-01T12:00:02Z [METRIC] endpoint=/api/login latency=45ms status=200 user_id=948` (Extract this)
*Corresponding CSV output line:*
`2023-10-01T12:00:02Z,/api/login,45,200`

**Phase 2: Aggregation and Log Rotation**
Create a Python script at `/home/user/aggregator.py` that reads `/home/user/parsed_metrics.csv`.
For each unique `endpoint`, calculate the 90th percentile (P90) latency. Use the nearest-rank method for percentiles (if the index is not an integer, round up to the nearest integer index. For example, the 90th percentile of 10 sorted items is the 9th item, i.e., index 8 in 0-indexed arrays).

The script must initialize a standard Python `logging` logger with a `RotatingFileHandler`. 
- Log file path: `/home/user/dashboard.log`
- Max bytes per file: `150` bytes
- Backup count: `3` (This should result in files like dashboard.log, dashboard.log.1, etc.)
- Log format string: `%(message)s`

For each unique endpoint (sorted alphabetically by endpoint name), log an INFO level message in exactly this format:
`Endpoint <endpoint> P90: <value>ms`

**Phase 3: JSON Dashboard Output**
At the end of the script, dump the calculated P90 latencies into a JSON file at `/home/user/dashboard_summary.json`. 
The format must be a single JSON object where keys are the endpoints and values are the integer P90 latencies.
Example: `{"/api/login": 45, "/api/logout": 12}`

Please write and execute the necessary commands and scripts to achieve this state. Automated tests will check the contents of `/home/user/parsed_metrics.csv`, the rotated log files starting with `/home/user/dashboard.log`, and the `/home/user/dashboard_summary.json` file.