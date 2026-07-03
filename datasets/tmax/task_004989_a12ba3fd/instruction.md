You are a Database Reliability Engineer (DBRE) investigating performance issues and lock contention in a local SQLite database used to track backup metadata. Concurrent writers are experiencing "database is locked" timeouts because analytical queries are performing full table scans and holding shared locks for too long.

The database is located at `/home/user/backups_meta.db`. 
It has two tables:
1. `servers` (`id` INTEGER PRIMARY KEY, `hostname` TEXT, `region` TEXT)
2. `backups` (`id` INTEGER PRIMARY KEY, `server_id` INTEGER, `timestamp` TEXT, `size_bytes` INTEGER, `status` TEXT)

Your task consists of two parts:

**Part 1: Schema Optimization**
Analyze the schema and create a SQL script at `/home/user/optimize.sql` that creates the necessary indexes to optimize the analytical query described in Part 2. The index(es) should specifically target the columns used for partitioning, ordering, and filtering to eliminate full table scans. Execute this SQL script against the database to apply the indexes.

**Part 2: Analytical Data Pipeline**
Write a Python script at `/home/user/analyze_backups.py` that queries the SQLite database to identify the exact moment a server's running total of "SUCCESS" backup sizes crosses a specific threshold. 

Your Python script must:
1. Use a single SQL query with a **Window Function** to calculate the running total of `size_bytes` for "SUCCESS" backups, partitioned by `server_id` and ordered by `timestamp` ascending.
2. Filter the results within the pipeline to find the *first* backup for each server where the running total of `size_bytes` strictly exceeds `500,000,000` bytes.
3. Join with the `servers` table to get the `hostname`.
4. Output the results as a JSON array to `/home/user/report.json`.

The JSON file must be formatted strictly as a list of objects, ordered alphabetically by `hostname`. Each object must have exactly these keys:
- `hostname` (string)
- `crossing_timestamp` (string, the timestamp of the backup that pushed the running total over the threshold)
- `running_total_bytes` (integer)

Example of expected JSON format:
```json
[
  {
    "hostname": "db-server-01",
    "crossing_timestamp": "2023-10-15T08:00:00Z",
    "running_total_bytes": 520000000
  }
]
```

Make sure your Python script runs successfully and generates `/home/user/report.json`.