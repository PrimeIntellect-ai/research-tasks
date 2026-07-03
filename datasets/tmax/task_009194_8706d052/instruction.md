You are an IT log analyst investigating intermittent server issues. You've received a CSV export of system metrics, but the data pipeline that generated it is known to be buggy. Specifically, some logs contain embedded newlines in their text fields, which breaks naive line-by-line processing, and timestamps are in inconsistent formats.

Your task is to write a Go program that robustly processes this CSV, validates the metrics, normalizes the timestamps, and enforces a data quality gate.

**Input:**
A CSV file located at `/home/user/system_metrics.csv`.
The CSV has the following headers: `timestamp,server_id,cpu_pct,ram_mb,event_details`

**Requirements for your Go program (`/home/user/process_metrics.go`):**

1. **Robust Parsing:** Use Go's standard `encoding/csv` package to parse the file. You must correctly handle rows where the `event_details` column contains embedded newlines (these will be wrapped in double quotes in the CSV).
2. **Timestamp Alignment:** The `timestamp` column contains mixed formats. It will either be in `YYYY-MM-DD HH:MM:SS` (assume UTC) or standard RFC3339 format. Your program must normalize all valid timestamps to strict RFC3339 format (e.g., `2023-10-12T14:30:00Z`).
3. **Constraint-Based Validation:** A row is considered **valid** if AND ONLY IF:
   - The timestamp can be parsed.
   - `cpu_pct` is a valid floating-point number between `0.0` and `100.0` (inclusive).
   - `ram_mb` is a valid integer strictly greater than `0`.
4. **Data Separation:** 
   - Write all **valid** rows to `/home/user/valid_metrics.csv` (include the header row). Valid rows must have their timestamps replaced with the normalized RFC3339 version.
   - Write all **invalid** rows to `/home/user/invalid_metrics.csv` (include the header row). Write the invalid rows exactly as they appeared (do not normalize the broken timestamps).
5. **Quality Gate:** Track the percentage of invalid rows (excluding the header from the total row count).
   - If **strictly greater than 20.0%** of the data rows are invalid, your program must print `QUALITY_GATE_FAILED` to standard output and exit with status code `1`.
   - Otherwise, print `QUALITY_GATE_PASSED` to standard output and exit with status code `0`.

**Execution:**
Once you have written the code, compile and run it to process `/home/user/system_metrics.csv` and generate the output files. Leave the output files and the source code in `/home/user/`.