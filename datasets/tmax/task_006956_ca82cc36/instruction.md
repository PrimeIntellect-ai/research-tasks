You are a log analyst investigating anomalous traffic patterns. We have an upstream ETL job that occasionally fails and retries, which produces duplicate event records in our logs. The retried events have slightly offset timestamps and different node IDs.

Your task is to write a Python script that builds a micro-pipeline to process these raw logs, clean the data, deduplicate the retry events, and compute rolling traffic statistics.

**Input Data:**
A CSV file located at `/home/user/raw_events.csv` with the following headers:
`raw_ts,usr,req_path,bytes,node_id`

**Processing Requirements:**
1. **Timestamp Parsing & Alignment:** The `raw_ts` field contains a mix of integer UNIX epochs (seconds) and ISO8601 UTC strings (e.g., `1970-01-01T00:16:40Z`). Convert all of these to integer UNIX epoch seconds. Sort all records chronologically by this parsed timestamp.
2. **Normalization:** Standardize the `req_path` field by converting it to lowercase and removing any trailing slashes (e.g., `/App/Login/` becomes `/app/login`). Ensure `bytes` is treated as an integer.
3. **Deduplication:** To filter out the ETL retry duplicates, iterate through your sorted and normalized events. Drop any event if a prior event with the *exact same* `usr` and *normalized* `req_path` was observed within the last 5 seconds (i.e., `current_ts - previous_ts <= 5`).
4. **Rolling Statistics:** For each *kept* (deduplicated) event, compute a rolling sum of the `bytes` field for all kept events (across all users/paths) that occurred in the 60-second window ending at the current event's timestamp (i.e., inclusive window `[current_ts - 60, current_ts]`).

**Output:**
Write the processed data to `/home/user/clean_metrics.jsonl` (JSON Lines format). 
Each line must be a valid JSON object representing a kept event with exactly these keys:
- `ts` (integer epoch seconds)
- `usr` (string)
- `req_path` (string, normalized)
- `bytes` (integer)
- `rolling_bytes_60s` (integer)

Do not include any external dependencies outside the Python Standard Library.