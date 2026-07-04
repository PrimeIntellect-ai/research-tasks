As a log analyst, you are investigating an unstable ETL job that occasionally crashes and retries, producing duplicate and fragmented log entries. You have been provided a raw log file in long format at `/home/user/etl_metrics.csv`.

Your objective is to clean the data, reshape it, compute rolling statistics to find anomalies, mask sensitive information, and produce a final report. Write and execute a Python script to accomplish this.

Here are the precise steps you must follow:
1. **Deduplication & Reshaping**: The input CSV has columns `timestamp`, `ip_address`, `metric_name`, and `metric_value`. Due to ETL retries, there are duplicate entries. Reshape the data into a wide format where the index is `timestamp` and `ip_address`, and the columns are the unique `metric_name`s. If there are duplicate `metric_value`s for the same timestamp, IP, and metric name, keep the **maximum** value.
2. **Imputation**: After reshaping, some metric values might be missing (NaN). Sort the data by `ip_address` then `timestamp` (ascending). For each `ip_address`, forward-fill (`ffill`) any missing metric values. 
3. **Rolling Statistics**: For the metric named `cpu_usage`, compute a 3-period rolling mean for each `ip_address` (this means the current row and the 2 preceding rows for that IP). If there are fewer than 3 periods available for an IP, the rolling mean should be NaN.
4. **Anomaly Detection**: Flag an anomaly if a row has a valid (non-NaN) `cpu_usage` rolling mean, and its actual `cpu_usage` value is **strictly greater than** 1.2 times its rolling mean (i.e., > 20% spike over the rolling average).
5. **Data Masking**: Anonymize the `ip_address` by replacing it with its SHA-256 hash (hexadecimal digest).
6. **Output**: Save the flagged anomalies to `/home/user/anomalies.csv`. 
   The output CSV must contain exactly these columns in this order: `timestamp`, `masked_ip`, `cpu_usage`, `cpu_rolling_mean`.
   Round the `cpu_usage` and `cpu_rolling_mean` to exactly 2 decimal places before saving. Do not include the pandas index in the CSV (use `index=False`).

Example output format (`/home/user/anomalies.csv`):
```csv
timestamp,masked_ip,cpu_usage,cpu_rolling_mean
2023-10-01T10:15:00,a1b2c3d4...,85.00,60.50
```