You are a log analyst investigating sudden performance degradations on our web servers. You have been provided with a large server log file at `/home/user/access_logs.jsonl`. We need to extract anomalous requests based on latency spikes, but due to privacy compliance, we must first mask the user IP addresses.

Write a Python script to process the logs and extract the anomalies. Your solution must adhere to the following requirements:

1. **Large-file streaming**: Process `/home/user/access_logs.jsonl` line by line. Do not load the entire file into memory at once. Each line is a JSON object with keys: `timestamp`, `ip`, `latency_ms`, and `status`.
2. **Data masking**: Replace the final octet of every IPv4 address with `XXX` (e.g., `192.168.1.105` becomes `192.168.1.XXX`).
3. **Windowed aggregation**: Maintain a rolling average of `latency_ms` for the *previous* 50 requests. For the first request, the rolling average is undefined. For requests 2 to 50, use the average of all preceding requests.
4. **Anomaly detection**: A request is considered an anomaly if its `latency_ms` is strictly greater than 3 times the rolling average of the previous requests. (Do not evaluate the first request as an anomaly).
5. **Multi-format writing**: Save the anomalous requests to a CSV file at `/home/user/latency_anomalies.csv`. The CSV must have exactly the following header: `timestamp,masked_ip,latency_ms,rolling_avg`. 
   - Round the `rolling_avg` to exactly 2 decimal places in the CSV (e.g., `105.40`).

Do not include any external libraries outside of the Python standard library.