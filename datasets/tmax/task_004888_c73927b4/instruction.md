You are a data engineer building a log processing ETL pipeline. You have a raw log file located at `/home/user/data/raw_logs.jsonl` containing JSON lines of web server access data. The logs come from different servers, so the timestamps are in different time zones and formats. They also contain sensitive Personal Identifiable Information (PII) that needs to be masked.

Your task is to write a Go program (`/home/user/etl.go`) that reads the raw logs, applies specific transformations, writes the processed records to `/home/user/data/processed_logs.jsonl`, and generates a pipeline monitoring file at `/home/user/data/metrics.json`.

**Data Processing Requirements:**
1. **Timestamp Alignment**: Parse the `timestamp` field. The input can be in either standard `RFC3339` format (e.g., `2023-10-12T14:30:00+02:00`) or Apache Common Log format (e.g., `12/Oct/2023:12:30:00 +0000`). Convert all parsed times to UTC and output them strictly in `RFC3339` format (e.g., `2023-10-12T12:30:00Z`).
2. **Data Masking (IP)**: Mask the `ip_address` field (which is always an IPv4 address) by replacing the last octet with `0` (e.g., `192.168.1.45` becomes `192.168.1.0`).
3. **Data Masking (Email)**: The `user_email` field must be masked by replacing everything before the `@` symbol with exactly three asterisks `***`. Rename this field to `masked_email` in the output. Omit the original `user_email` field.
4. **Feature Extraction (URL)**: Parse the `url` field and extract only the path component. Store this in a new field called `path`. Do not include the query string or domain. Omit the original `url` field.
5. **Feature Extraction (Speed)**: Create a new field `speed` based on the `response_time_ms` integer field:
   - "fast": strictly less than 100
   - "medium": 100 to 500 (inclusive)
   - "slow": strictly greater than 500

**Output Schema for `processed_logs.jsonl`:**
Each line must be a JSON object containing exactly these fields:
`timestamp` (string), `ip_address` (string), `masked_email` (string), `path` (string), `response_time_ms` (integer), `speed` (string).

**Pipeline Logging / Monitoring:**
Your program must track the run metrics and output a single JSON object to `/home/user/data/metrics.json` containing exactly these integer fields:
- `total_processed`: Total number of log lines successfully processed.
- `fast_count`: Number of logs categorized as "fast".
- `medium_count`: Number of logs categorized as "medium".
- `slow_count`: Number of logs categorized as "slow".

Write the Go code, build it or run it via `go run`, and ensure both `processed_logs.jsonl` and `metrics.json` are generated successfully. You may use standard Go libraries; no external packages are required.