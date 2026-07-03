You are an expert data engineer. We have a legacy system that exports messy CSV logs. We need you to build a Python pipeline to process these logs, deduplicate them using a proprietary legacy tool, and serve the cleaned data via a local REST API.

Here are the requirements:

1. **Data Parsing and Normalization**:
   - You are provided a raw log file at `/home/user/raw_logs.csv`. This file is encoded in `UTF-16LE`.
   - The CSV has three columns: `Timestamp`, `UserID`, and `Message`.
   - Note: The `Message` field often contains embedded newlines. You must properly parse the CSV without silently dropping or truncating these multi-line records.
   - You must normalize all `Timestamp` values into UTC ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`. The input timestamps are a mix of US format (`MM/DD/YYYY HH:MM:SS`) and raw integer Unix Epochs (in seconds). Assume all non-Epoch times are already in UTC.

2. **Deduplication using Legacy Hasher**:
   - We deduplicate records based on a proprietary hash of the timestamp and user ID.
   - A compiled binary is available at `/app/legacy_hasher`.
   - For every record, you must invoke the binary exactly as follows: `/app/legacy_hasher "<NORMALIZED_TIMESTAMP>|<UserID>"` (e.g., `/app/legacy_hasher "2023-10-01T12:00:00Z|U105"`).
   - The binary will output a 32-character hex string.
   - Use this hex string to deduplicate records. If multiple records generate the same hash, keep only the *first* one encountered in the file.

3. **API Service**:
   - Write a Python script `/home/user/server.py` that loads the cleaned, deduplicated data and starts an HTTP server on `127.0.0.1:8080`.
   - Provide a GET endpoint at `/api/logs` that accepts a query parameter `user` (e.g., `/api/logs?user=U105`).
   - The endpoint must return a JSON payload: `{"logs": [{"timestamp": "...", "message": "..."}, ...]}` ordered by timestamp ascending.
   - The server should run in the foreground when executed. Start the server in the background using `nohup python3 /home/user/server.py &` so the verification process can query it.

4. **Pipeline Scheduling**:
   - Create a cron-formatted file at `/home/user/pipeline.cron` containing a single line that schedules `/home/user/pipeline.py` to run every 15 minutes.

Do not use root privileges. Standard libraries and `flask` or `fastapi` are available if you install them via pip.