You are a log analyst investigating a recent traffic spike on your server. You have been provided with a raw access log file in JSON-Lines format.

The log file is located at `/home/user/server_logs.jsonl`. 

However, there is a problem: a misconfigured client has been injecting malformed unicode escape sequences (e.g., `\uXYZ1`, which are not valid hexadecimal) into the user-agent strings. These malformed sequences cause standard JSON parsers (like strict `jq` or Python's `json`) to crash.

Your task is to analyze these logs to find anomalous traffic spikes by following these exact steps:

1. **Data Cleaning**: Filter the log file to completely discard any lines containing malformed unicode escape sequences. A valid unicode escape sequence is exactly `\u` followed by 4 hexadecimal characters (0-9, a-f, A-F). If a line contains `\u` followed by characters that do not form a 4-digit hex code, it is malformed and the entire line must be discarded.

2. **Time-based Bucketing**: For the remaining valid JSON lines, extract the `timestamp` field (which is in ISO 8601 format, e.g., `2023-10-01T14:35:12Z`). Group the logs into 1-hour buckets. Your bucket identifier should be the date and hour, formatted exactly as `YYYY-MM-DDTHH` (e.g., `2023-10-01T14`). Calculate the total count of valid logs in each hourly bucket.

3. **Rolling Statistics**: Compute a 3-hour rolling average of the log counts for each hour. The rolling average for a given hour should be the mean of the counts from the *strictly preceding* 1 to 3 hours. 
   - If 3 preceding hours of data are available, average all 3.
   - If only 1 or 2 preceding hours are available (at the start of the timeline), average what is available.
   - If no preceding hours are available, the rolling average is `0.0`.
   - Ensure the rolling average is rounded/formatted to exactly 1 decimal place (e.g., `10.0`, `15.3`).
   - Note: Include hours with `0` valid logs in your rolling window if they fall sequentially within the preceding 3 hours of an active log bucket, but you only need to output/calculate anomalies for hours that actually have logs.

4. **Anomaly Detection**: An hour is flagged as an anomaly if its log count is *strictly greater* than `2.0` times its preceding rolling average, AND the log count is at least `10`.

5. **Reporting**: Write the anomalous hours to a CSV file located at `/home/user/anomalies.csv`. The CSV must have exactly this header: `hour,count,rolling_avg`. 
   For example:
   ```csv
   hour,count,rolling_avg
   2023-10-01T15,45,12.5
   ```

You may use Python, Bash, or any CLI tools to complete this task.