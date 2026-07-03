You are tasked with fixing and orchestrating an ETL pipeline for a rudimentary configuration management system. Our servers dump their configuration state changes into audit logs. Unfortunately, the current logging mechanism frequently retries failed uploads, resulting in duplicated entries in the log files. 

You need to build a robust, idempotent Bash-based pipeline that cleans these logs, deduplicates them, extracts the latest state, and is scheduled to run continuously.

Here are the requirements:

1. **Write an ETL Bash Script (`/home/user/process_configs.sh`):**
   - The script must read all `.log` files in the `/home/user/raw_logs/` directory.
   - It must parse valid log lines using Regular Expressions and ignore malformed lines.
   - A valid log line strictly follows this format (including spaces):
     `[{ISO-8601-TIMESTAMP}] {SERVER_NAME} - ACTION: {ACTION} - KEY: {KEY} - VALUE: {VALUE}`
     *Example:* `[2023-11-01T14:32:01Z] prod-db-01 - ACTION: UPDATE - KEY: max_connections - VALUE: 500`
   - It must perfectly deduplicate the records. Because of retries, the exact same entry (same timestamp, server, action, key, and value) might appear multiple times across or within the log files. Keep only one instance of each.
   - The script must output a comma-separated values (CSV) file to `/home/user/output/config_state.csv`.
   - The CSV must have the header: `timestamp,server,action,key,value`
   - The output CSV must be sorted chronologically by timestamp (ascending). If timestamps are identical, sort alphabetically by server name, then by key.
   - The script must be idempotent. Running it multiple times should result in the exact same `/home/user/output/config_state.csv` file without accumulating duplicates. Make sure the script is executable.

2. **Write a Stratification Script (`/home/user/latest_state.sh`):**
   - This script must read the generated `/home/user/output/config_state.csv`.
   - It must output a new CSV file to `/home/user/output/latest_state.csv` (with the same header).
   - The output must contain *only the single most chronologically recent* entry for each unique `(server, key)` combination.
   - Sort the final output alphabetically by `server` name, then by `key`.
   - Make sure the script is executable.

3. **Pipeline Scheduling:**
   - Create a text file at `/home/user/cron_schedule.txt`.
   - This file must contain exactly one cron expression line that schedules `/home/user/process_configs.sh` to run every 5 minutes (as the user `user`). Do not install it into the live crontab, just provide the correct line in the file.

Ensure all output directories are created if they do not exist. You are free to use standard Unix utilities (like `grep`, `sed`, `awk`, `sort`, etc.) within your Bash scripts.