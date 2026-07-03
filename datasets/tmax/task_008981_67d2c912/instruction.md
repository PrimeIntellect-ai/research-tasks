You are a log analyst investigating sudden performance degradations in an API. 

You have been provided with a CSV file at `/home/user/api_latency.csv` containing chronological logs of API requests. The file has no header and contains three comma-separated columns:
`timestamp, endpoint_path, latency_in_ms`

Your task is to identify latency anomalies using a rolling statistics approach. 
Write a script or use command-line tools (like `awk`, `sed`, or pure `bash`) to process the file and find anomalous logs based on these exact rules:

1. **Rolling Window:** For each line, calculate the rolling average latency of the strictly *previous 5 lines*. Do not include the current line's latency in this calculation.
2. **Warm-up Period:** Do not evaluate the first 5 lines for anomalies, as they do not have a full window of 5 previous lines. However, they will be used to build the window for the 6th line onwards.
3. **Anomaly Condition:** A line is considered an anomaly if its `latency_in_ms` is strictly greater than `2.0` times the rolling average of the previous 5 lines.
4. **Window Updating:** Anomalous values *must* still be included in the rolling window for subsequent lines.
5. **Output:** Write the identified anomalies to a new file at `/home/user/anomalies.csv`. The output format must be:
`timestamp,endpoint_path,latency_in_ms,rolling_average`
Format the `rolling_average` exactly to 1 decimal place (e.g., `48.4`).

Example:
If the previous 5 latencies were 45, 50, 48, 52, and 47, the rolling average is 48.4. If the current latency is 110, it is an anomaly because 110 > (48.4 * 2.0). 
The output line would be: `2023-10-01T10:00:06,/login,110,48.4`

Process `/home/user/api_latency.csv` and generate `/home/user/anomalies.csv` meeting all these requirements.