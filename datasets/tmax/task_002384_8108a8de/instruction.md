You are tasked with analyzing a large configuration change log for a fleet of servers. The system tracks every time a configuration value is modified. 

The log file is located at `/home/user/config_changes.log`. It is potentially very large, so you must stream the file line-by-line rather than loading it entirely into memory.

Each line in the log has the following format:
`[YYYY-MM-DD HH:MM:SS] USER:<username> CONFIG:<key>=<value>`

For example:
`[2023-10-24 14:23:01] USER:admin CONFIG:max_connections=500`

Write a Python script at `/home/user/process_configs.py` that does the following:
1. **Large-file streaming & Regex**: Iterates through `/home/user/config_changes.log` line-by-line. Use a regular expression to extract the date/time, the configuration key, and the configuration value.
2. **Time-based bucketing**: Truncate the timestamp to the hour (e.g., `2023-10-24 14`).
3. **Hash-based deduplication**: Within each hourly bucket, keep track of unique configuration changes (the exact `key=value` pair). If a `key=value` pair appears multiple times in the same hour, only record it once (keep the first occurrence).
4. **Aggregation Output**: Output a JSON file to `/home/user/hourly_summary.json` where the keys are the hourly buckets (e.g., `"2023-10-24 14"`) and the values are lists of the unique `key=value` strings that occurred in that hour. The lists of strings must be sorted alphabetically.
5. **Pipeline logging**: While running, your script must write a single log line to `/home/user/pipeline.log` in the format: `Processed X lines successfully.` where X is the total number of lines processed.

Execute your Python script once it is written so the output files are generated.