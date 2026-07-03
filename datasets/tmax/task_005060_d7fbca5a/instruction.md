You are a log analyst investigating performance degradation across a fleet of web servers. You have been given a dataset of raw server logs, and you need to build a high-performance Python processing pipeline to identify anomalous requests.

The raw log files are located in `/home/user/logs/raw/`. There are dozens of log files, each representing a different server.

Each line in the log files follows this format:
`[YYYY-MM-DD HH:MM:SS] IP_ADDRESS HTTP_METHOD ENDPOINT HTTP_STATUS RESPONSE_TIME_MS`
Example:
`[2023-10-24 14:22:10] 192.168.1.100 GET /api/v1/data 200 45`

Your task is to write a Python script at `/home/user/analyze_logs.py` that processes these logs and extracts the anomalies. 

The script must perform the following:
1. **Parallel Processing**: You must use Python's `multiprocessing` or `concurrent.futures` module to read and parse the log files in parallel. 
2. **Feature Extraction & Standardization**: 
   - Parse each log line to extract the timestamp, IP address, endpoint, and response time.
   - Convert the timestamp into a standard UNIX epoch integer (UTC). Assume the log timestamps are already in UTC.
3. **Normalization (Z-Score)**:
   - Calculate the global mean and standard deviation of the `RESPONSE_TIME_MS` for *each unique ENDPOINT* across the entire dataset. (Note: This will likely require a two-pass approach or aggregating stats first).
   - If an endpoint has fewer than 2 requests or a standard deviation of 0, its requests cannot be considered anomalous (ignore them).
   - Calculate the Z-score for every request's response time: `z_score = (response_time - mean_for_endpoint) / std_dev_for_endpoint`.
4. **Filtering**:
   - Filter out and keep only the requests that are strictly greater than 3.0 standard deviations above the mean (`z_score > 3.0`).
5. **Output**:
   - Save the anomalous requests to a CSV file at `/home/user/logs/anomalies.csv`.
   - The CSV must have the following exact header: `timestamp_epoch,ip_address,endpoint,response_time_ms,z_score`
   - Round the `z_score` to exactly 3 decimal places (e.g., `3.142`).
   - The final CSV must be sorted primarily by `timestamp_epoch` (ascending) and secondarily by `ip_address` (ascending).

Constraints:
- Only use standard Python libraries (e.g., `os`, `csv`, `datetime`, `multiprocessing`, `statistics`, `math`). Do not use `pandas` or `numpy` (they are not installed).
- Ensure your output file matches the expected format precisely.