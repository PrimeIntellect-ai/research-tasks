You are a log analyst investigating patterns in a system that frequently generates multiline error traces.

You have been provided with a raw log file at `/home/user/system_logs.csv` containing four columns: `timestamp`, `log_level`, `user_id`, and `message`. 
Because some log messages contain raw stack traces or multiline dumps, the `message` column often contains embedded newlines wrapped in double quotes. Standard line-by-line grep pipelines have been silently corrupting or dropping these entries.

Your task is to write an executable Bash script at `/home/user/process_logs.sh` (you may use embedded Python, `awk`, or other standard CLI tools within the script) that reads `/home/user/system_logs.csv` and produces a cleaned, stratified sample of high-priority events saved to `/home/user/sampled_errors.csv`.

The processing pipeline must perform the following operations:
1. **Filtering**: Retain only rows where the `log_level` is `ERROR` or `CRITICAL`.
2. **Constraint Validation**: Drop any row where the `timestamp` does not exactly match the ISO-8601 format: `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2023-10-05T14:30:00Z`). Years should be constrained between 2020 and 2024.
3. **Normalization**: Convert all `user_id` values to uppercase.
4. **Deduplication**: There are recurring identical error messages. Deduplicate the logs based *strictly* on the exact `message` content. If multiple logs have the identical `message` text, keep only the earliest one (based on chronological order of the `timestamp`).
5. **Stratified Sampling**: From the cleaned, deduplicated logs, extract exactly the 2 earliest `ERROR` events and the 2 earliest `CRITICAL` events.
6. **Output**: Write these 4 events (plus the header row) to `/home/user/sampled_errors.csv` in valid CSV format (quoting the `message` field). Output the 2 `ERROR` logs first (sorted chronologically), followed by the 2 `CRITICAL` logs (sorted chronologically).

Make sure the output file strictly matches the standard CSV format with embedded newlines correctly preserved. Run your script to generate `/home/user/sampled_errors.csv`.