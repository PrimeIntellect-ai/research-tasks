You are tasked with setting up an automated anomaly detection pipeline for a configuration manager. The system logs the number of active `worker_threads` every minute into a CSV file. You need to write a script that processes this time-series data to detect anomalous spikes, and then schedule it using `cron`.

Here are your instructions:

1. A CSV file is located at `/home/user/config_metrics.csv` containing two columns: `timestamp` and `worker_threads`.
2. Write a Python script at `/home/user/detect_anomalies.py` that reads this CSV and performs the following data transformations:
   - Compute a 5-period rolling mean and 5-period rolling standard deviation (using sample standard deviation, ddof=1) for the `worker_threads` column.
   - Calculate the rolling Z-score for each row: `(worker_threads - rolling_mean) / rolling_std`.
   - Ignore any rows where the rolling statistics are `NaN` (i.e., the first 4 rows).
   - Filter the data to find anomalies where the Z-score is strictly greater than `1.5`.
3. The script should output the detected anomalies to a JSON file at `/home/user/anomalies.json`. The JSON file must contain a single array of objects, where each object represents an anomaly and has exactly these keys:
   - `timestamp` (string)
   - `worker_threads` (integer)
   - `z_score` (float, rounded to exactly 2 decimal places)
4. Execute your script once manually so the `/home/user/anomalies.json` file is generated.
5. Set up a user cron job (using `crontab`) that schedules this script (`/usr/bin/env python3 /home/user/detect_anomalies.py`) to run every 5 minutes (e.g., `*/5 * * * *`).

Ensure your script handles standard CSV parsing and accurately calculates the rolling statistics. You may use standard Python libraries or `pandas` if installed.