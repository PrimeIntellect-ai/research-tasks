You are a Database Reliability Engineer (DBRE) tasked with analyzing our database backup logs to detect anomalies in backup sizes. 

We have a raw log file located at `/home/user/backup_logs.jsonl` containing JSON lines of backup metadata. Some of the automated loggers have been malfunctioning, so the file contains malformed data.

Your task is to build a Python-based data pipeline that accomplishes the following:

1. **Output Schema Validation**: Read `/home/user/backup_logs.jsonl` and filter out invalid rows. A valid row must strictly contain all of the following fields with the correct types:
   - `backup_id` (string)
   - `timestamp` (string, ISO8601 format like "2023-10-01T10:00:00Z")
   - `status` (string, exactly either "SUCCESS" or "FAILURE")
   - `size_bytes` (integer)
   - `database_name` (string)
   If a row is missing any field, contains extra fields, or has incorrect types (e.g., a string instead of an integer for `size_bytes`), discard it.

2. **Database Ingestion**: Load the validated, strictly formatted rows into an SQLite database located at `/home/user/backups.db` in a table named `backup_history`.

3. **Analytical Aggregation (Window Functions)**: We need to detect sudden spikes in backup sizes, which could indicate runaway log tables or compromised data. 
   - Consider **only** backups with a `status` of "SUCCESS".
   - For each successful backup, calculate its "expected size" as the average `size_bytes` of the **previous two** successful backups for the *same* `database_name`, ordered by `timestamp`. (If a backup has fewer than 2 preceding successful backups, it does not have an expected size and cannot be evaluated for a spike).
   - Calculate the "spike size" as the current backup's `size_bytes` minus its expected size.

4. **Reporting Anomalies**: For each database, find the single successful backup with the **maximum spike size**, provided that the maximum spike size is strictly greater than `0`.
   - Write these results to a CSV file at `/home/user/anomalies.csv`.
   - The CSV must have exactly these columns, in this order: `database_name,backup_id,spike_size`
   - Sort the CSV alphabetically by `database_name`.
   - The `spike_size` should be formatted as a floating-point number with exactly 1 decimal place (e.g., `150.5`).

You may use standard Python libraries (e.g., `sqlite3`, `json`, `csv`). Put all your implementation logic in a script and execute it to generate the final `anomalies.csv`.