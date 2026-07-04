You are a Database Reliability Engineer (DBRE) analyzing database backup performance across multiple shards.

You have been provided with an SQLite database at `/home/user/backups.db` containing a single table `backup_logs` with the following schema:
- `id` (INTEGER PRIMARY KEY)
- `shard_id` (TEXT)
- `backup_date` (TEXT, ISO 8601 format)
- `duration_seconds` (INTEGER)
- `status` (TEXT, e.g., 'SUCCESS', 'FAILED')

Your task is to write a Rust program in `/home/user/backup_analyzer` that performs the following steps:

1. **Index Strategy Design:** 
   Connect to `/home/user/backups.db` and execute a SQL statement to create an optimal composite index named `idx_shard_status_date` on `(shard_id, status, backup_date)` to speed up the subsequent queries.

2. **Window Functions and Analytical Aggregation:**
   Write a query that calculates two metrics for each `shard_id`:
   - `avg_duration`: The average `duration_seconds` of the **last 3** successful backups (status = 'SUCCESS') ordered by `backup_date`.
   - `failure_count`: The total number of failed backups (status = 'FAILED') across all time for that shard.
   
   Filter the results to include only shards where the `avg_duration` is strictly greater than `300.0` AND the `failure_count` is at least `1`.

3. **Output Schema Validation:**
   Structure the filtered results as a JSON array of objects with keys `"shard_id"` (string), `"avg_duration"` (float), and `"failure_count"` (integer).
   Before writing the output, your Rust program must validate the JSON array against the JSON schema provided at `/home/user/schema.json` (you can use the `jsonschema` crate).
   If validation passes, write the output to `/home/user/report.json`.

Please create the Rust project, write the code, and execute it to produce `/home/user/report.json`.