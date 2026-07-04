You are a log analyst investigating patterns in system and application logs. You have two log files in different formats and need to normalize, deduplicate, and aggregate them.

Your tasks are:
1. Parse logs from two files:
   - `/home/user/logs/app.log`: Space-separated, format `[YYYY-MM-DD HH:MM:SS] LEVEL MESSAGE`
   - `/home/user/logs/sys.csv`: CSV format, format `timestamp,level,message` (timestamp is `YYYY-MM-DDTHH:MM:SSZ`)

2. Deduplication:
   - Combine the entries from both files.
   - Deduplicate globally based on the exact text of the `MESSAGE`.
   - If a message appears multiple times, only keep the chronologically FIRST occurrence across all logs. Discard the later occurrences.

3. Time-based Bucketing & Aggregation:
   - Align the timestamp of each kept log entry to the nearest 15-minute bucket, rounded down (e.g., `10:05:12` becomes `10:00`, `10:14:59` becomes `10:00`, `10:17:00` becomes `10:15`).
   - Count the number of `ERROR` and `WARNING` entries in each 15-minute bucket.

4. Output:
   - Create a summary CSV at `/home/user/report.csv` with the exact header: `bucket,ERROR,WARNING`.
   - Format the bucket column as `YYYY-MM-DD HH:MM`.
   - Sort the output chronologically by bucket.

5. Pipeline Scheduling:
   - Write a valid cron expression to a file at `/home/user/cron.txt` that schedules a script named `/home/user/process.sh` to run exactly at the top of every hour (minute 0). The file should contain only the single cron configuration line.

Constraints:
- You must write a shell script or run standard CLI commands (e.g., awk, sed, sort, bash) to process the data.