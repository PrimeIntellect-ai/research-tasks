You are acting as a log analyst investigating a recent system degradation. We have a raw CSV log file at `/home/user/raw_logs.csv` containing web server access logs. Your objective is to build a Python-based data pipeline that processes these logs, computes rolling statistics, detects anomalous periods of high error rates, anonymizes the anomalous records, and exports them to a SQLite database.

Please complete the following tasks:

1. **Environment Setup:**
   Create a virtual environment at `/home/user/venv` and install `pandas` and any other required Python libraries.

2. **Rolling Statistics & Anomaly Detection:**
   Write a Python script (e.g., `/home/user/pipeline.py`) that reads `/home/user/raw_logs.csv`. The CSV has the following columns: `timestamp` (ISO8601), `ip_address`, `endpoint`, `status_code`, and `response_time_ms`.
   - Ensure the data is sorted chronologically by `timestamp`.
   - Create a boolean or binary indicator for "error", defined as `status_code >= 400`.
   - Compute the **5-minute trailing rolling average** of the error indicator based on the `timestamp` for each row. This represents the "rolling error rate". (Hint: Use pandas `rolling` with a time-based window of '5min' or '5T'. Ensure the timestamp is the index or specified in the `on` parameter).
   - Flag a log entry as an **anomaly** if its computed 5-minute rolling error rate is strictly greater than `0.15` (15%).

3. **Data Masking (Anonymization):**
   For all log entries flagged as anomalies, anonymize the `ip_address` by replacing the last octet of the IPv4 address with `0` (e.g., `192.168.1.45` becomes `192.168.1.0`). Store this in a new column called `masked_ip`.

4. **Database Bulk Export:**
   Export ONLY the anomalous rows to a SQLite database located at `/home/user/anomalies.db`.
   - The table must be named `anomalous_logs`.
   - It must contain exactly the following columns in this order: `timestamp`, `masked_ip`, `endpoint`, `status_code`, `response_time_ms`, and `rolling_error_rate`.
   - The `rolling_error_rate` should be rounded to 4 decimal places before insertion.

Execute your pipeline so that `/home/user/anomalies.db` is completely populated according to these rules.