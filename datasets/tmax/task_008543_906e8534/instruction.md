You are a log analyst investigating an increase in server errors. You need to build a lightweight data processing pipeline in Python to analyze server logs, bucket them by time, and apply a quality gate to flag problematic time periods.

The raw log file is located at `/home/user/data/server_logs.txt`.
Each line in the log file follows this exact format:
`[YYYY-MM-DD HH:MM:SS] IP_ADDRESS METHOD PATH HTTP_VERSION STATUS_CODE`
Example: `[2023-10-25 14:22:10] 192.168.1.1 GET /api/data 1.1 500`

Write a Python script at `/home/user/analyze_logs.py` and execute it. The script must act as a sequential pipeline with the following requirements:

1. **Time-based Bucketing**: Parse the logs and bucket the requests by the hour. Truncate the timestamp to the hour (e.g., `2023-10-25 14:22:10` becomes the bucket `2023-10-25 14:00`).
2. **Aggregation**: For each hourly bucket, calculate the total number of requests and the total number of server errors (HTTP status codes 500 and above).
3. **Validation Checkpoint (Quality Gate)**: Evaluate each bucket. If the error rate (errors / total requests) is **strictly greater than 5.0%** (0.05), the bucket fails the quality gate and should be flagged.
4. **Pipeline Output**: 
   - Create a JSON file at `/home/user/flagged_hours.json` containing a list of dictionaries for all flagged hours. 
   - Each dictionary must have the following keys: `"hour"` (string, format `YYYY-MM-DD HH:00`), `"total"` (integer), `"errors"` (integer), and `"error_rate"` (float, rounded to exactly 4 decimal places). 
   - The JSON list must be sorted chronologically by hour.
5. **Pipeline Logging**: The script must log its progress to `/home/user/pipeline.log`. It must append lines indicating stage completions:
   - `[INFO] Stage: Extract and Bucket - Completed`
   - `[INFO] Stage: Aggregate - Completed`
   - `[INFO] Stage: Validation Gate - Completed`
   - `[INFO] Pipeline finished. Flagged hours: X` (where X is the integer count of flagged hours).

Run the script to produce the final outputs.