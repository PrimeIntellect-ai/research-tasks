You are a log analyst investigating a recent system degradation. You have been provided with log files from two different web servers that handle a load-balanced application. The logs are in different formats and contain duplicate entries due to a retry mechanism in the load balancer.

Your task is to write a Bash script at `/home/user/analyze_logs.sh` that processes these logs, aligns their formats, deduplicates the entries, extracts minute-by-minute metrics, and detects the exact minute a specific performance anomaly began.

**Log Files (located in `/home/user/logs/`):**
1. `server_A.log` - Format: `YYYY-MM-DD HH:MM:SS|IP|STATUS|RESPONSE_TIME_MS|PAYLOAD_HASH`
   (Timestamps are in UTC)
2. `server_B.log` - Format: `EPOCH_TIME,IP,STATUS,RESPONSE_TIME_MS,PAYLOAD_HASH`

**Requirements for `/home/user/analyze_logs.sh`:**
1. **Timestamp Alignment & Parsing:** Read both files and normalize `server_B.log` into the same pipe-delimited format as `server_A.log`. Convert the epoch timestamps in `server_B.log` to UTC `YYYY-MM-DD HH:MM:SS`.
2. **Deduplication:** Combine the normalized logs. Due to load balancer retries, there are exact duplicate rows across the unified dataset (where all fields, including the normalized timestamp, match exactly). Deduplicate the dataset so only unique rows remain.
3. **Feature Extraction:** Aggregate the deduplicated logs by minute (`YYYY-MM-DD HH:MM`). For each minute, calculate:
   - The total number of server errors (STATUS >= 500)
   - The average response time (RESPONSE_TIME_MS) of all requests in that minute (integer, truncated/floor).
4. **Anomaly Detection:** An "anomaly" is defined as a minute where:
   - The number of server errors (STATUS >= 500) is strictly greater than 3.
   - AND the average response time for that minute is strictly greater than 1000 ms.
5. **Output:** Identify the chronologically *first* minute that satisfies the anomaly condition. Your bash script must output exactly one line to `/home/user/anomaly_report.txt` in the following format:
   `ANOMALY_MINUTE: YYYY-MM-DD HH:MM, ERRORS: <count>, AVG_TIME: <avg_time>ms`

**Example Output:**
`ANOMALY_MINUTE: 2024-01-15 08:12, ERRORS: 5, AVG_TIME: 1450ms`

Ensure your script is executable and performs all steps when run without arguments. Do not hardcode the expected answer; your script must dynamically compute it from the logs.