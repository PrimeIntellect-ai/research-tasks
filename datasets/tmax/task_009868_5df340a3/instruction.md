You are tasked with writing a C program to analyze configuration management logs and detect anomalous bursts in configuration changes.

A system logs configuration changes from various servers into a CSV file located at `/home/user/config_changes.csv`. 
The file has no header and contains three comma-separated columns:
`timestamp,server_id,impact_score`
- `timestamp`: Unix epoch time (integer).
- `server_id`: A string representing the server.
- `impact_score`: An integer representing the magnitude of the configuration change.

Your objective is to write a C program at `/home/user/analyze.c` that compiles to `/home/user/analyze`. When executed, it must read `/home/user/config_changes.csv` and produce an output file at `/home/user/anomalies.csv` following these data processing rules:

1. **Time-Based Bucketing:**
   Group the `impact_score` values into 1-hour (3600 seconds) buckets.
   A bucket's starting timestamp `T` is calculated as `timestamp - (timestamp % 3600)`.
   The sequence of buckets must be continuous, starting from the bucket of the earliest timestamp in the input file, up to the bucket of the latest timestamp in the input file. If a bucket has no events, its total impact is 0.

2. **Rolling Statistics Calculation:**
   For each bucket `T`, calculate the moving average of the total impact over the **previous 3 hours** (i.e., buckets `T-10800`, `T-7200`, and `T-3600`).
   - If a bucket has fewer than 3 preceding buckets (e.g., the very first bucket), calculate the average over the *available* preceding buckets. 
   - For the very first bucket, since there are no preceding buckets, the moving average is `0.00`.

3. **Anomaly Detection:**
   A bucket is flagged as an anomaly (`is_anomaly = 1`) if BOTH of the following conditions are met:
   - Its total impact strictly exceeds `2.0 * moving_average` of the preceding 3 buckets.
   - Its total impact strictly exceeds `50`.
   Otherwise, `is_anomaly = 0`.

4. **Output Format:**
   The output file `/home/user/anomalies.csv` must contain a header and have the following format:
   `bucket_start,total_impact,moving_avg,is_anomaly`
   - `bucket_start`: The starting Unix timestamp of the bucket.
   - `total_impact`: Integer sum of impacts for that hour.
   - `moving_avg`: Float, formatted to exactly 2 decimal places (e.g., `33.33`).
   - `is_anomaly`: `1` or `0`.

Write, compile, and execute the C program to generate the required output file.