You are a data analyst managing a daily data pipeline for server performance metrics. The raw time-series data is dumped into `/home/user/data/raw/` as CSV files, but the format is inconsistent.

Your task is to create a multi-stage Bash processing pipeline script at `/home/user/process_timeseries.sh` and set up its scheduling configuration.

**Requirements:**

1. **Write the Pipeline Script (`/home/user/process_timeseries.sh`):**
   - The script must read all CSV files in `/home/user/data/raw/`. 
   - The raw CSV files have the format: `timestamp,metric_name,value,status`
   - **Filter:** Keep only the rows where `status` is exactly `OK`.
   - **Normalize (Tokenize/Transform):** 
     - Extract only the date portion (YYYY-MM-DD) from the `timestamp` column. Note: Some timestamps use slashes (`YYYY/MM/DD...`), which must be normalized to hyphens (`YYYY-MM-DD`). 
     - Convert the `metric_name` to entirely lowercase.
   - **Output:** Save the normalized valid rows to `/home/user/data/processed/metrics_summary.csv` in the format: `date,metric_name,value`. (No header is needed).
   - **Logging:** After generating the summary, append a log entry to `/home/user/logs/pipeline.log` in exactly this format:
     `[YYYY-MM-DD HH:MM:SS] Pipeline completed. Processed <N> valid records.` 
     *(Replace YYYY-MM-DD HH:MM:SS with the current system time using `date +'%Y-%m-%d %H:%M:%S'`, and `<N>` with the integer count of rows written to the summary CSV).*

2. **Schedule the Pipeline:**
   - Create a crontab configuration file at `/home/user/crontab.txt`.
   - Add a single cron expression to run your script (`/home/user/process_timeseries.sh`) every day at exactly 2:00 AM.

Ensure your script is executable (`chmod +x`). You can use standard bash tools like `awk`, `sed`, `grep`, `date`, `wc`, etc. Execute your script once manually to ensure it processes the existing raw data and generates the log and output file correctly.