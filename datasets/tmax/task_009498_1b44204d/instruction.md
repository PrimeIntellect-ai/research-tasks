You are acting as a backup administrator trying to audit our archived log data. 

We have a directory at `/home/user/archives` that contains historical logs organized by year, month, and day subdirectories. The logs themselves are compressed as `.json.gz` files to save space. 

Inside these gzipped files are JSON Lines (JSONL) records. Each line is a valid JSON object representing a log event. Some of these events represent system crashes and contain a `stack_trace` field, which is a multi-line string.

Your task is to write and execute a Python script to do the following:
1. Recursively traverse the `/home/user/archives` directory to find all `.json.gz` files.
2. Stream and read the contents of these compressed files directly (do not extract them to disk).
3. Parse the JSON records and identify all events where the `"level"` field is exactly `"FATAL"`.
4. For each FATAL event, calculate the number of lines in the `"stack_trace"` string. (An empty string has 0 lines, a string with no newline characters has 1 line, etc.)
5. Output the results to a CSV file located at `/home/user/fatal_summary.csv`.

The output CSV must have the following exact headers: `timestamp,service,trace_lines`.
The rows in the CSV must be sorted chronologically by the `timestamp` field in ascending order.

Please write the Python script, save it to `/home/user/audit.py`, and execute it to generate the final CSV file.