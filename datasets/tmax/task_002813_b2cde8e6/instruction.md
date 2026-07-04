You are a log analyst investigating a recent failure in an ETL data pipeline. The pipeline experienced several timeouts and retries, resulting in multiple log files containing duplicated, overlapping event records. Furthermore, due to a misconfigured logging agent, some of the logs contain corrupted byte sequences (mixed character encodings).

Your task is to write a Python script that processes these logs, cleans up the encoding errors, deduplicates the records, and outputs a single, chronologically sorted, clean log file.

**Input Data:**
There are four log files located in `/home/user/logs/`:
- `etl_retry_0.log`
- `etl_retry_1.log`
- `etl_retry_2.log`
- `etl_retry_3.log`

Each file contains JSON strings (one per line). The JSON objects have the following schema:
`{"timestamp": "YYYY-MM-DDTHH:MM:SS", "event_id": "uuid-string", "user_id": 123, "payload": "text", "retry_count": int}`

**Requirements for your Python script:**
1. **Parallel Processing:** You must use Python's `multiprocessing` or `concurrent.futures` module to read and parse the log files in parallel.
2. **Character Encoding Handling:** The files contain invalid UTF-8 bytes. You must read the files as binary and decode them as UTF-8, replacing invalid characters with the standard Unicode replacement character (`U+FFFD` / ``).
3. **Hash-based Deduplication:** The same `event_id` may appear multiple times across the different files due to the ETL retries. You must deduplicate the records based on the `event_id`. If duplicate `event_id`s are found, you must keep the record with the **highest** `retry_count`.
4. **Sorting:** After deduplicating, sort the final collection of records chronologically by `timestamp` (ascending). If timestamps are identical, tie-break by sorting alphanumerically by `event_id` (ascending).
5. **Output Format:** Write the final sorted, deduplicated records to `/home/user/cleaned_logs.jsonl`. Ensure that each line is a valid JSON object. To guarantee deterministic output for automated verification, write the JSON objects with their keys sorted alphabetically (e.g., using `json.dumps(record, sort_keys=True)`).

Write and execute the Python script to produce `/home/user/cleaned_logs.jsonl`.