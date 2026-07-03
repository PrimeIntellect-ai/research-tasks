You are a data engineer responsible for a lightweight ETL pipeline using only bash and standard coreutils (awk, sed, date, sort, etc.).

Your task is to create a shell script at `/home/user/run_etl.sh` that processes two different raw log files, normalizes their data, aligns their timestamps, and merges them into a single sorted CSV. Finally, the script must log its execution.

Here are the requirements:

1. **Input Files**: 
   - `/home/user/raw/app.log`: Contains application errors.
     Format: `[YYYY-MM-DD HH:MM:SS] severity: message`
     Example: `[2023-10-15 10:05:00] error: Connection reset`
   - `/home/user/raw/sec.log`: Contains security warnings.
     Format: `MM/DD/YYYY HH:MM:SS SEVERITY: message`
     Example: `10/15/2023 10:04:30 WARN: Failed auth`

2. **Processing Steps (Pipeline)**:
   - Create the output directory `/home/user/processed/` if it does not exist.
   - Parse the dates from both log files and convert them to Unix Epoch timestamps (seconds since 1970-01-01 00:00:00 UTC).
   - Extract the severity level and normalize it to uppercase (e.g., "error" -> "ERROR", "WARN" -> "WARN").
   - Track the source of the log ("app" for `app.log`, "sec" for `sec.log`).
   
3. **Output format**:
   - Merge the processed records from both files.
   - Sort the merged records chronologically (numerically by epoch timestamp, oldest first).
   - Write the output to `/home/user/processed/alerts.csv`.
   - The output must include a header row and be formatted exactly as:
     `epoch,severity,source`
     Example row: `1697364300,ERROR,app`

4. **Pipeline Logging**:
   - After successfully writing the CSV, your script must append a log entry to `/home/user/etl.log`.
   - The log entry must be in this exact format:
     `[<CURRENT_EPOCH_TIMESTAMP>] SUCCESS: processed <N> alerts`
     Where `<CURRENT_EPOCH_TIMESTAMP>` is the current Unix epoch time when the script finishes, and `<N>` is the total number of data rows (excluding the header) written to the CSV.

Make sure your script is executable. You can assume that the `date` command available is GNU `date`.