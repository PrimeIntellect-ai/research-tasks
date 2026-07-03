You are a log analyst investigating sudden performance degradations in a web application. You have been provided with a large server access log, and you need to build a data pipeline to stream, analyze, and summarize this log.

Write a Python script at `/home/user/analyze_logs.py` and execute it to process the log file located at `/home/user/server_logs.log`. 

The log file contains one request per line in the following space-separated format:
`TIMESTAMP IP_ADDRESS HTTP_METHOD URL STATUS_CODE RESPONSE_TIME_MS`
Example: `2024-03-15T10:00:00Z 192.168.1.50 GET /api/data 200 145`

Your Python script must perform the following tasks:

1. **Large-file Streaming:** Read the log file line-by-line. Do not load the entire file into memory (assume the real file could be hundreds of gigabytes).
2. **Pipeline Logging:** Configure Python's standard `logging` module to write to `/home/user/pipeline.log`. 
   - Write `[INFO] Pipeline started` at the beginning.
   - Write `[INFO] Processed X lines` every 5,000 lines (e.g., 5000, 10000).
   - Write `[INFO] Pipeline finished` at the end.
3. **Rolling Statistics Computation:** Maintain a sliding window of the last exactly **500** response times. 
   - The window starts empty. Once you have read the 500th line, the window is "full".
   - For every line processed *after* the window becomes full (from the 501st line onwards), calculate the arithmetic mean (average) of the response times in the current window.
   - If this rolling average is **strictly greater than 800.0 ms**, it is considered an anomaly.
   - Append anomalies to `/home/user/anomalies.csv` with the format `TIMESTAMP,ROLLING_AVG_MS`. Round the rolling average to exactly 2 decimal places. Include a header row: `timestamp,rolling_avg`.
4. **Sorting and Grouping:** While streaming, track the following metrics for each unique IP address:
   - Total number of requests.
   - Total number of errors (any `STATUS_CODE` >= 400).
   - Sum of all response times (to calculate the average later).
5. **Database Bulk Export:** Once the file is fully processed, calculate the average response time for each IP (Sum / Total Requests). Create an SQLite database at `/home/user/ip_summary.db` and insert this aggregated data using a bulk import method (e.g., `executemany`).
   - Create a table named `ip_stats` with the schema: `ip TEXT, total_requests INTEGER, total_errors INTEGER, avg_resp_time REAL`.

Ensure your script creates all the required output files and handles the streaming efficiently. Run your script to generate `/home/user/anomalies.csv`, `/home/user/ip_summary.db`, and `/home/user/pipeline.log`.