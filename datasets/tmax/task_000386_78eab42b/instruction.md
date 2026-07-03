You are a log analyst investigating anomalous patterns from an ETL job that failed and retried, resulting in a dirty dataset containing duplicates and inconsistent formats. You need to write a Python pipeline to clean, deduplicate, and summarize these logs.

**Input Data:**
There is a JSON file at `/home/user/raw_data/retried_logs.json`. It contains a JSON array of log event objects.
Each object has the following keys: `timestamp`, `user`, `action`, and `ingestion_time`.
Due to the retries, the same event may appear multiple times. The `ingestion_time` will differ between retries, but the core event (`timestamp`, `user`, `action`) represents the exact same occurrence.
Furthermore, the `timestamp` field was written by different systems and can be in one of three formats:
1. Unix epoch time (integer or string representing seconds, e.g., `1682859321`)
2. ISO 8601 string (e.g., `"2023-04-30T12:55:21Z"`)
3. Slash-separated string (e.g., `"2023/04/30 12:55:21"`) (Assume UTC)

**Your Objectives:**

1. **Timestamp Alignment:** Parse and normalize all `timestamp` fields into a strict ISO 8601 format string (e.g., `"YYYY-MM-DDTHH:MM:SSZ"`). All times are in UTC.
2. **Hash-based Deduplication:** Deduplicate the records. Two records are considered identical if they yield the same SHA256 hash. The hash must be computed over a single UTF-8 string formatted exactly as: `"{user}|{action}|{normalized_timestamp}"`. 
   Keep only the first occurrence of each unique event (based on the original order in the JSON array). Discard the `ingestion_time` field entirely.
3. **Pipeline Output:** Write the cleaned, deduplicated logs to `/home/user/clean_logs.jsonl` (JSON Lines format). Each line must be a JSON object containing: `event_hash` (the SHA256 hex digest), `timestamp` (the normalized ISO string), `user`, and `action`. Sort the output JSON lines by `timestamp` in ascending order.
4. **Template-based Reporting:** Generate a summary report at `/home/user/report.txt`. The report must strictly follow this template:
   ```
   ETL Log Processing Report
   =========================
   Total raw records processed: {{ total_records }}
   Total unique records retained: {{ unique_records }}
   Total duplicates removed: {{ duplicate_records }}
   Most active user (by unique records): {{ most_active_user }}
   ```
   (If there's a tie for most active user, pick the one that comes first alphabetically).

Write the Python script, execute it to process the data, and ensure both output files (`/home/user/clean_logs.jsonl` and `/home/user/report.txt`) are generated correctly according to the specifications above.