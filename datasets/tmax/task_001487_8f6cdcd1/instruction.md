You are a log analyst investigating patterns in a web application's logs. The logs are stored in JSON-lines format, but there is a problem: a bug in the application caused it to sometimes write malformed unicode escape sequences (e.g., `\u12G4` or `\u001`), which causes standard JSON parsers like `jq` to fail.

Your task is to write a Bash script at `/home/user/process_logs.sh` that processes the raw log file located at `/home/user/raw_logs.jsonl` and performs the following operations:

1. **Validation and Filtering (Regex & Constraint Validation):**
   Filter the `raw_logs.jsonl` file to separate valid logs from invalid ones.
   An invalid log line is defined as any line containing a literal backslash followed by the letter `u` (`\u`) that is **not** immediately followed by exactly four hexadecimal digits (`[0-9a-fA-F]{4}`).
   Save all valid lines to `/home/user/clean_logs.jsonl` and all invalid lines to `/home/user/invalid_logs.jsonl`. Keep the original order.

2. **Rolling Statistics Computation:**
   Using the `clean_logs.jsonl` file, compute a rolling average of the `time` field (response time) exclusively for lines where the `path` field is exactly `"/api/data"`. Use a window size of 3. For the first two elements, the rolling average should be computed over the available elements.
   The output should be written to `/home/user/rolling_stats.csv` with the following format:
   ```csv
   ts,rolling_avg
   <ts_value_1>,<avg_1_formatted_to_2_decimal_places>
   <ts_value_2>,<avg_2_formatted_to_2_decimal_places>
   ...
   ```
   You may assume the `ts` values are integers and `time` values are integers. You can use standard tools like `awk`, `sed`, or `grep`. Do not use `jq` as it may struggle or you might want to rely on text processing. (Actually, `jq` is fine for `clean_logs.jsonl` since it's valid JSON, but `awk` can do the rolling average).

3. **Template-Based Text Generation:**
   Generate a summary report at `/home/user/report.md` using the exact template below, replacing the bracketed placeholders with the computed integer values:
   ```markdown
   # Log Analysis Report
   
   Total valid logs: {VALID_COUNT}
   Total invalid logs: {INVALID_COUNT}
   Max response time for /api/data: {MAX_TIME}
   ```
   `{MAX_TIME}` is the maximum `time` value among the valid logs for the `"/api/data"` path.

Ensure your script is executable (`chmod +x /home/user/process_logs.sh`) and run it so the output files are generated.