You are a Database Reliability Engineer. We export our backup metadata from a NoSQL document store to a JSON Lines file every night. You need to write a Python script to analyze this data and generate a consolidated report simulating an aggregation pipeline.

The raw data is located at `/home/user/backups_metadata.jsonl`. Each line is a JSON object representing a backup job, with the following schema:
- `backup_id` (string): Unique identifier for the backup.
- `database_name` (string): Name of the database backed up.
- `region` (string): The deployment region (e.g., "us-east-1").
- `status` (string): The backup status ("SUCCESS", "FAILED", or "IN_PROGRESS").
- `timestamp` (string): ISO 8601 formatted date and time.
- `size_bytes` (integer): Size of the backup in bytes.

Write a Python script at `/home/user/analyze_backups.py` that reads this file and implements the equivalent of a NoSQL aggregation pipeline to produce a report with the following rules:
1. **Filter**: Include only backups with a `status` of "SUCCESS".
2. **Group**: Group the records by `region` and then by `database_name`.
3. **Aggregate**: For each database in each region, determine the `latest_backup` (the most recent timestamp) and calculate the `total_size_bytes` (the sum of `size_bytes` across all successful backups for that specific database in that region).
4. **Sort**: Sort the final results first by `region` in ascending alphabetical order, and then by `total_size_bytes` in descending order.
5. **Output**: Save the results as a formatted JSON array to `/home/user/backup_report.json`.

The output file `/home/user/backup_report.json` must be a valid JSON array of objects with exactly these keys:
- `region`
- `database_name`
- `latest_backup`
- `total_size_bytes`

Execute your script to ensure the `backup_report.json` file is created.