You are a log analyst investigating a recent series of distributed system failures. The raw logs from our regional servers have been aggregated, but they are messy. Some timestamps were corrupted during transmission and marked as `MISSING`, and the error messages contain multilingual text and Unicode emojis. 

Your objective is to write a Bash script at `/home/user/process_logs.sh` that cleans, filters, and consolidates these logs.

**Input Data:**
The raw logs are located in `/home/user/raw_logs/` as several CSV files (e.g., `us.csv`, `eu.csv`, `ap.csv`).
The format of each file is: `TIMESTAMP,SEVERITY,REGION,MESSAGE`

**Task Requirements:**
1. **Parallel Processing:** Your script must process all `.csv` files in the `/home/user/raw_logs/` directory in parallel (e.g., using background jobs `&` and `wait`, or `xargs -P`).
2. **Timestamp Interpolation (Imputation):** Some rows have `MISSING` in the `TIMESTAMP` column. You must replace `MISSING` with the integer average (mean) of the timestamp from the immediately preceding row and the immediately succeeding row in that same file. 
    * *Note:* You can assume the first and last rows of a file never have a missing timestamp, and there are never two consecutive `MISSING` timestamps. Timestamps are standard Unix epochs. Use standard integer division.
3. **Unicode & Language Filtering:** After interpolating the timestamps, filter the logs to keep ONLY the rows that meet at least one of the following conditions:
    * The `SEVERITY` is exactly `CRITICAL`.
    * The `MESSAGE` contains the Unicode stop sign emoji `🛑` (U+1F6D1).
    * The `MESSAGE` contains the Japanese word for failure: `故障`
4. **Consolidation:** The filtered, interpolated rows from all files must be combined into a single output file at `/home/user/critical_events.csv`.
5. **Sorting:** The final `/home/user/critical_events.csv` must be sorted numerically in ascending order by the `TIMESTAMP` column.

**Execution:**
Once your script is written, run it to generate `/home/user/critical_events.csv`. Ensure the script has executable permissions. We will verify the contents of the final CSV file.