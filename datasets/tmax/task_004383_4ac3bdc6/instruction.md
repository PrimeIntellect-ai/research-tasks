You are a data engineer building ETL pipelines. We have a system that generates diagnostic logs in CSV format, but the system occasionally writes multi-line tracebacks into the `message` column, resulting in embedded newlines within quoted CSV fields. Standard text processing tools like simple `awk` or `grep` pipelines often silently drop or mangle these rows.

Your task is to create a robust Bash script that acts as an ETL pipeline to process these time-series logs, aggregate them, and schedule the pipeline.

**Requirements:**

1.  **Write the ETL Script:** Create a bash script at `/home/user/process_logs.sh`. The script must read the input file `/home/user/incoming/data.csv`.
2.  **Filter and Extract:** The script must filter the rows to include ONLY records where the `metric_name` is exactly `memory_leak_bytes`. It must properly handle quoted fields containing embedded newlines (you may use tools like `python3`, `csvkit`, `perl`, etc., which are available in standard environments, invoked from your bash script).
3.  **Time-based Bucketing and Aggregation:** 
    *   Extract the `timestamp`, `hostname`, and `value` columns.
    *   Truncate the `timestamp` to the start of the hour (e.g., `2023-10-12 08:45:10` becomes `2023-10-12 08:00:00`).
    *   Calculate the maximum `value` (as an integer) per hour, per `hostname`.
4.  **Formatting and Output:**
    *   Write the aggregated results to `/home/user/output/max_memory.csv`.
    *   The output file must include a header row exactly as: `hour,hostname,max_value`.
    *   The rows must be sorted chronologically by `hour` (ascending), and then alphabetically by `hostname` (ascending).
    *   Fields in the output CSV should be comma-separated without quotes.
5.  **Execution and Scheduling:**
    *   Make the script executable and run it once so the output file is generated.
    *   Schedule this script to run at minute 0 of every hour using the user's crontab.
    *   Dump your current crontab to a file at `/home/user/cron_backup.txt` (e.g., `crontab -l > /home/user/cron_backup.txt`) so your scheduling can be verified.

**Input Data Specifications:**
*   Location: `/home/user/incoming/data.csv`
*   Header: `timestamp,hostname,metric_name,value,message`
*   `timestamp` format: `YYYY-MM-DD HH:MM:SS`

Make sure your final output file strictly adheres to the required format and sorting, and that all embedded newline edge cases are correctly parsed.