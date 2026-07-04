You are a data scientist cleaning a telemetry dataset. You have been given a JSON-lines file at `/home/user/telemetry.jsonl`. However, the system that generated this file had a bug, and some lines contain invalid unicode escape sequences (e.g., `\u123Z`) which will cause standard JSON parsers to break.

Write a Python script at `/home/user/clean_ts.py` and run it to process this file according to the following requirements:
1. Read the `/home/user/telemetry.jsonl` file line by line.
2. Attempt to parse each line as JSON. If a line throws a JSON decoding error, completely ignore and skip that line.
3. For the successfully parsed lines, mask the `user_ip` field by replacing its value with the literal string `***`.
4. Ensure the records are sorted chronologically by the `ts` (timestamp) field in ascending order.
5. Compute a rolling average of the `metric` field over a window of 3 periods (inclusive of the current row). If there are fewer than 3 periods available (e.g., the first two rows), compute the average using the available periods.
6. Detect anomalies: Add a boolean field `is_anomaly`. Set it to `True` if the current `metric` value is strictly greater than its rolling average plus `20.0`. Otherwise, set it to `False`.
7. Save the resulting dataset to `/home/user/cleaned.csv` as a CSV file with the exact following columns: `ts,user_ip,metric,rolling_avg,is_anomaly`.
8. Round `rolling_avg` to 2 decimal places in the output CSV.

Run your script so that `/home/user/cleaned.csv` is generated successfully.