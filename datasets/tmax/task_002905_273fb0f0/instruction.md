You are a data analyst managing a time-series data pipeline. You receive continuous batches of CSV log files that contain timestamps, user IDs, and JSON-like payload strings. However, some payloads are corrupted due to a faulty upstream JSON-lines parser that fails and writes malformed unicode escape sequences into the CSV fields.

Your goal is to build a robust data sanitization and aggregation pipeline.

**Step 1: Extract Configuration**
There is an image file located at `/app/instructions.png`. Extract the configuration parameters from this image. It contains specific instructions on the time-bucketing interval you must use for aggregation, and the column name you must use for hash-based deduplication.

**Step 2: Build the Sanitizer (Adversarial Filter)**
Create an executable script at `/home/user/sanitizer`. 
- It must read standard input (stdin) and write to standard output (stdout).
- It must act as a filter for the CSV rows (assume a standard CSV with a header: `timestamp,user_id,payload`).
- It must drop *only* the rows where the `payload` column contains a malformed unicode escape sequence (i.e., a literal `\u` that is NOT immediately followed by exactly four valid hexadecimal digits).
- We have provided test data:
  - `/app/corpus/clean/`: Contains CSV files with perfectly valid rows (including valid unicode escapes like `\u004A`). Your script must preserve these rows exactly as they are (including the header).
  - `/app/corpus/evil/`: Contains CSV files where every data row has a malformed unicode escape (e.g., `\u123Z`, `\u99`, `\u-abc`). Your script must drop all data rows from these files (it may keep or drop the header, but no evil data rows should pass).

**Step 3: Aggregation Pipeline**
Create a script at `/home/user/aggregate.sh` that takes a sanitized CSV file as its first argument.
This script must:
1. Tokenize and normalize the `payload` text (convert to lowercase).
2. Compute an MD5 hash of the normalized payload and deduplicate rows that have the identical hash.
3. Bucket the `timestamp` (ISO 8601 format) into the time intervals specified in `/app/instructions.png`.
4. Output a summary CSV to stdout with the format: `time_bucket,unique_event_count`.

**Step 4: Scheduling**
Create a cron file at `/home/user/pipeline.cron` that schedules `/home/user/aggregate.sh` to run every 15 minutes, processing `/tmp/latest.csv`.

Ensure your scripts are executable. You may use Python, Bash, awk, or any standard Linux tools available.