You are a Database Reliability Engineer (DBRE) responsible for analyzing backup systems.

We have a local SQLite database at `/home/user/backups.db` that tracks all our database backup jobs. You need to write a Go program to extract specific analytical insights from it.

Your task:
1. Analyze the schema of `/home/user/backups.db` to understand the relationships between the databases and the backup jobs.
2. Write a Go program at `/home/user/analyze.go`. This program must:
   - Accept a single command-line argument: the `cluster_name` (e.g., `go run /home/user/analyze.go "eu-central-1"`).
   - Use parameterized queries to prevent SQL injection when querying the cluster name.
   - Use SQLite window functions (specifically `LAG()`) to compute the difference in backup sizes.
   - For every database in the specified cluster, find the **most recent successful** backup (`status = 'SUCCESS'`). 
   - Calculate the size difference in bytes between this most recent successful backup and the **immediately preceding successful backup** for the same database. (If there is no previous successful backup, the difference should be `null` or `0` depending on your implementation, but output `0` in the JSON).
   - Write the results to `/home/user/report.json`.

The output `/home/user/report.json` must exactly match this JSON array schema:
```json
[
  {
    "database_name": "string",
    "latest_backup_time": "string (YYYY-MM-DD HH:MM:SS)",
    "latest_size_bytes": 12345,
    "size_diff_from_previous": 123
  }
]
```
Sort the JSON array alphabetically by `database_name`.

Once you have written the script, run it for the cluster `"eu-central-1"`.