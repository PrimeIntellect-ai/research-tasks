You are a log analyst investigating API performance anomalies across several microservices. You have been given a raw, slightly corrupted JSONL (JSON Lines) log file at `/home/user/logs/raw_requests.jsonl`.

Your goal is to build a Python pipeline that cleans this data, computes a rolling statistical baseline for latency, and exports the anomalous requests to a database. 

Please perform the following steps:

1. **Hash-based Deduplication**: Read the JSONL file. Multiple retries might have logged the exact same payload. Deduplicate the records by computing the MD5 hash of the `request_payload` field. If multiple logs have the same payload hash, keep only the one with the earliest `timestamp`.
2. **Constraint-based Validation**: Discard any records that do not meet these constraints:
   - `status_code` must be an integer and exactly one of: 200, 201, 400, 401, 403, 404, 500, 502, 503.
   - `response_time_ms` must be a numeric value strictly greater than 0.
   - `timestamp` must be a valid integer.
3. **Rolling Statistics Computation**: For the valid, deduplicated records, group them by `endpoint`. Sort the records within each group by `timestamp` in ascending order. For each record, calculate the rolling average of `response_time_ms` over a window of the last 5 requests for that specific endpoint (including the current request). If fewer than 5 requests are available (e.g., the first 4 requests), calculate the average over all available requests up to that point.
4. **Anomaly Detection**: Flag a request as an anomaly if its `response_time_ms` is strictly greater than `1.5 * rolling_average`.
5. **Database Export**: Export *only* the flagged anomalous records into a new SQLite database at `/home/user/logs/anomalies.db`. Create a table named `flagged_logs` with the following columns: `timestamp` (INTEGER), `endpoint` (TEXT), `status_code` (INTEGER), `response_time_ms` (REAL), and `rolling_avg` (REAL, rounded to 2 decimal places).

Ensure the final SQLite database is saved correctly at `/home/user/logs/anomalies.db`.