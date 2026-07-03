You are a data engineer responsible for fixing an ETL pipeline issue. You have a set of daily CSV log files located in `/home/user/data/logs/`. 

Recently, a bug in the upstream exporter caused embedded newlines in the `notes` column to be output raw (without quotes or escapes). Because of this, many rows are improperly split across multiple lines, which silently drops or corrupts data in our downstream naive line-by-line processors.

Your task is to build a multi-stage Bash pipeline using standard CLI tools (like `awk`, `sed`, `grep`, `sort`, etc.) to clean, normalize, deduplicate, and analyze this data.

Perform the following steps:
1. **Clean & Normalize**: Reconstruct the broken rows. You can assume that any line that does NOT begin with a valid date format (`YYYY-MM-DD`) or the exact word `date` (the header) is a continuation of the `notes` field from the preceding line. Merge these continuation lines with the preceding line, replacing the erroneous newline character with a single space.
2. **Deduplicate**: After repairing the rows, combine all the data from the CSV files. Remove any perfectly duplicate rows (ignoring duplicates of the header so only one header remains). 
3. **Sort**: Sort the final dataset (excluding the header, which should remain at the top) first by `date` (ascending) and then by `session_id` (ascending).
4. **Detect Anomaly**: We expect roughly the same number of events every day. However, one specific date experienced a severe pipeline drop and has fewer than 3 events in the cleaned, deduplicated dataset. 

**Outputs required**:
* Save the fully cleaned, deduplicated, and sorted dataset (including exactly one header row) to `/home/user/output/master_log.csv`.
* Identify the date with the anomalous drop in events (fewer than 3) and write ONLY that date (in `YYYY-MM-DD` format) to `/home/user/output/anomaly.txt`.

All necessary files are in `/home/user/data/logs/`. The target directory `/home/user/output/` already exists.