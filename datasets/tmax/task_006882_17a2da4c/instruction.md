You are a log analyst investigating suspicious login patterns. A messy application log file has been placed at `/home/user/app_logs.txt`. Your task is to write a Python script that processes this file, extracts structured data, filters out invalid and duplicate entries, and produces clean output files.

Requirements for the Python script:

1. **Extraction & Validation**:
   Process `/home/user/app_logs.txt` line by line. Use Regular Expressions to extract the following fields from lines that match this specific format:
   `[<timestamp>] ERROR from <ip_address>: User '<username>' failed to login (Code: <error_code>)`
   
   - `timestamp`: The date and time inside the brackets (e.g., `2023-10-25 10:00:01`).
   - `ip_address`: The IPv4 address (e.g., `10.0.0.1`).
   - `username`: The string inside the single quotes (e.g., `alice`).
   - `error_code`: The integer error code (e.g., `401`).

   Any line that does not strictly contain all these elements in this pattern must be considered invalid and dropped.

2. **Deduplication**:
   Sometimes the system writes the exact same log event multiple times. Deduplicate the valid parsed records. A record is a duplicate if it has the exact same `timestamp`, `ip_address`, `username`, and `error_code` as an earlier parsed record. Keep only the first occurrence.

3. **Output Clean Logs**:
   Save the valid, unique records to `/home/user/clean_logs.jsonl` in JSON Lines format. Each line must be a valid JSON object with the keys `"timestamp"`, `"ip_address"`, `"username"`, and `"error_code"`. `error_code` must be an integer; the others must be strings.

4. **Output Pipeline Logging**:
   Create a validation summary file at `/home/user/processing_summary.json`. It must be a standard JSON file containing exactly these three integer keys:
   - `"total_lines"`: Total number of lines read from the input file.
   - `"valid_lines"`: Number of lines that successfully matched the regex pattern.
   - `"unique_valid_lines"`: Number of valid lines remaining after deduplication.

Write and execute the script to produce both output files.