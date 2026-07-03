You are a log analyst investigating patterns in an application's distributed infrastructure. A previous data pipeline was failing because it silently dropped log entries containing embedded newlines (like stack traces). Your goal is to build a robust Python-based ETL pipeline that correctly parses the data, merges it with server metadata, and calculates rolling time-based statistics.

You have been provided with two input datasets:
1. `/home/user/app_logs.csv`: A CSV file containing application logs. Columns: `timestamp`, `server_id`, `log_level`, `message`. The `message` column contains quoted text that often spans multiple lines. All timestamps are in UTC (ISO8601 format).
2. `/home/user/server_meta.json`: A JSON file containing server metadata. It is a list of objects with keys: `server_id`, `region`, and `tier`.

Write a Python script at `/home/user/process_logs.py` that performs the following tasks:
1. **Extract & Clean**: Read the CSV and JSON files. Ensure that rows with embedded newlines in the CSV are correctly parsed and not dropped.
2. **Transform (Merge)**: Join the log entries with the server metadata on `server_id`. If a log entry has a `server_id` not found in the metadata, drop that row.
3. **Transform (Bucket & Aggregate)**: Group the joined data into 1-hour tumbling time windows based on the `timestamp` (e.g., `2023-10-01T10:00:00Z` to `2023-10-01T10:59:59Z`). For each time window and `region` combination, calculate the `total_logs` (count of all logs in that window/region) and `error_count` (count of logs where `log_level` is exactly `"ERROR"`). 
4. **Transform (Rolling Stats)**: For each `region`, calculate a 3-hour rolling average of the `error_count` (i.e., the average of the `error_count` for the current 1-hour window and the two preceding 1-hour windows). If previous windows have no data, treat their error count as 0 for the rolling average computation.
5. **Load**: Output the final aggregated data to `/home/user/rolling_stats.json`.

The output file `/home/user/rolling_stats.json` must be a JSON array of objects, sorted ascending by `region` (alphabetically) and then ascending by `window_start`. Each object must have exactly these keys:
- `window_start`: String, ISO8601 format (e.g., `"2023-10-01T10:00:00Z"`).
- `region`: String.
- `total_logs`: Integer.
- `error_count`: Integer.
- `rolling_3h_error_avg`: Float, rounded to exactly 2 decimal places.

You may install and use any Python libraries you need (e.g., `pandas`) using standard package managers. Run your script to generate the final JSON file.