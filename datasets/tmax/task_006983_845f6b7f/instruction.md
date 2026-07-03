You are a log analyst investigating performance degradation on a web server. 

You have been given a log file at `/home/user/app_logs.jsonl`. Each line is intended to be a JSON object representing a web request, containing `timestamp` (ISO 8601 string), `endpoint` (string), `response_time_ms` (integer), and `user_agent` (string). 

However, there is a problem: a bug in the logging library caused corrupted unicode escape sequences in the `user_agent` field (e.g., `\u002X`), which will cause standard JSON parsers like Python's `json.loads()` to crash.

Your task is to write a Python script to process this file and detect latency anomalies. You must:

1. Robustly parse the file to extract the `timestamp`, `endpoint`, and `response_time_ms` fields from each line, bypassing or fixing the corrupted JSON.
2. Group the requests by `endpoint`.
3. Within each endpoint group, sort the requests chronologically by `timestamp`.
4. For each request, calculate the rolling average `response_time_ms` of the **5 immediately preceding requests** for that same endpoint. (Do not include the current request in the average. If there are fewer than 5 preceding requests for an endpoint, do not compute an average and do not flag it as an anomaly).
5. Detect an anomaly if a request's `response_time_ms` is strictly greater than 3.0 times its calculated preceding rolling average.
6. Output the detected anomalies to a CSV file at `/home/user/anomalies.csv`.

The output CSV must have exactly these columns in order: `timestamp,endpoint,response_time_ms,rolling_avg`. 
Format `rolling_avg` to exactly 1 decimal place (e.g., `120.5`). 
Sort the final CSV rows chronologically by `timestamp`.

Ensure your Python script runs and successfully creates the `/home/user/anomalies.csv` file. You may install any standard packages (like pandas) if you need them, but the core text processing and logic must be implemented correctly.