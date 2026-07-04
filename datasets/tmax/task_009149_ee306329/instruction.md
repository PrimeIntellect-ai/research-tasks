You are an AI assistant helping a log analyst investigate server performance patterns. The analyst has collected server metric logs from different systems, but the data is in various formats and contains missing values due to sensor dropouts.

Your task is to build a Python data processing pipeline that normalizes, imputes, and summarizes this data.

**Data Sources:**
The logs are located in `/home/user/data/logs/` and come in three different formats:
1. `srv01_metrics.csv` (CSV format with header: `timestamp,server_id,cpu_temp`)
2. `srv02_metrics.json` (JSON array of objects with keys: `timestamp`, `server_id`, `cpu_temp`)
3. `srv03_metrics.jsonl` (JSON-Lines format, one JSON object per line)

**Pipeline Requirements:**
1. **Combine and Sort**: Read all three files, combine the records, and sort them chronologically by `timestamp` (integer UNIX epoch).
2. **Group**: Group the sorted records by `server_id`.
3. **Impute**: Some `cpu_temp` values are `null` (or empty strings in CSV). For each `server_id` group, sort by timestamp and interpolate the missing `cpu_temp` values using standard linear interpolation between the nearest previous and next valid temperatures. (You may assume the first and last records for each server always have valid temperatures).
4. **Template Generation**: For each `server_id`, generate a summary report text file at `/home/user/reports/<server_id>_report.txt` exactly matching this template:
```
Server: <server_id>
Total Records: <count>
Max Temp: <max_temp_formatted_to_2_decimal_places>
Average Temp: <avg_temp_formatted_to_2_decimal_places>
```
*(Example: `Max Temp: 45.00`)*

5. **Pipeline Logging**: As your script processes the data, it must append log messages to `/home/user/pipeline.log`. Write exactly one line per server processed, in alphabetical order of `server_id`, matching this exact format:
`[INFO] Successfully processed <server_id> with <count> records.`

**Execution**:
Write a Python script at `/home/user/process_logs.py` that implements this logic and run it. The final state should have the three report files in `/home/user/reports/` and the log file at `/home/user/pipeline.log`.