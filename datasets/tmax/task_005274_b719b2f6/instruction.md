You are a log analyst investigating a series of anomalies in a distributed application. You have received a raw log file `/home/user/raw_logs.jsonl` from globally distributed services. These logs contain mixed multi-language error messages (in varying Unicode normalization forms), performance metrics with missing data points, and occasional malformed lines.

Your task is to build a data processing pipeline that reads the raw logs, cleans the text, imputes missing values, calculates an anomaly score, and generates a formatted report of the top anomalies.

Here are the specific requirements for your processing pipeline:

1. **Validation & Quality Gates:**
   - Read `/home/user/raw_logs.jsonl`.
   - Skip any lines that are invalid JSON.
   - Any log entry missing the `timestamp` or `service` fields should be entirely discarded.

2. **Unicode Normalization:**
   - Extract the `message` field from valid logs.
   - Convert the `message` string to Unicode NFC (Normalization Form C). This is critical as the same characters are represented differently in the raw logs.

3. **Data Interpolation (Mathematical):**
   - The `metrics` object contains `response_time_ms` and `cpu_load`. Some of these values are `null` (missing).
   - Group the logs by the `service` field. Within each service, sort the logs strictly by `timestamp` in ascending order.
   - Impute any `null` metric values using **linear interpolation based on timestamps**. 
   - Formula for interpolation at missing time $T$: 
     $V = V_1 + (V_2 - V_1) \times \frac{T - T_1}{T_2 - T_1}$
     where $(T_1, V_1)$ is the closest prior valid data point and $(T_2, V_2)$ is the closest subsequent valid data point for that metric in the same service.
   - If a missing value occurs before the first valid value, use the first valid value (backfill). If it occurs after the last valid value, use the last valid value (forward-fill).
   - Keep interpolated values as floating-point numbers.

4. **Anomaly Scoring:**
   - For every valid, processed log entry, calculate an `anomaly_score` using the following mathematical formula:
     `score = (response_time_ms * 0.5) + (cpu_load * 100)`
   - If the NFC-normalized `message` contains the exact substring `[FATAL]`, add `1000` to the calculated score.

5. **Template-Based Generation:**
   - Identify the top 3 log entries with the highest `anomaly_score` across all services.
   - Generate a report at `/home/user/anomaly_report.txt` using the exact following template for each of the top 3 entries (sorted from highest score to lowest):
     `[{timestamp}] Service {service} score: {score:.2f} | Msg: {message}`
   - Ensure the score is formatted to exactly 2 decimal places.

You may use Python, Ruby, Perl, or standard bash tools (jq, awk) to accomplish this. Save your code and execute it so that `/home/user/anomaly_report.txt` is produced with the correct results.