You are a Database Reliability Engineer managing backups across a hybrid infrastructure. You have backup job metadata stored in a SQLite database and detailed transfer metrics exported from a MongoDB cluster into a JSON Lines format. 

Your task is to write a Python script `/home/user/db_report.py` that generates a consolidated backup failure and transfer report for a specific datacenter. 

The SQLite database is located at `/home/user/backups.db` and has the following schema:
- `servers` table: `id` (INTEGER PRIMARY KEY), `hostname` (TEXT), `datacenter` (TEXT)
- `backup_jobs` table: `job_id` (INTEGER PRIMARY KEY), `server_id` (INTEGER), `status` (TEXT), `timestamp` (DATETIME)

The detailed metrics export is located at `/home/user/nosql_metrics.jsonl`. Each line is a JSON document representing a chunk of data transferred, with the following structure:
`{"hostname": "server-1", "type": "backup", "bytes_transferred": 1048576, "duration_seconds": 15}`

Write a Python script `/home/user/db_report.py` that does the following:
1. Takes exactly one command-line argument: the `datacenter` name (e.g., `us-east-1`).
2. Connects to `/home/user/backups.db`.
3. Constructs and executes a parameterized SQL query (using a CTE and JOIN) to find all servers in the given datacenter that have at least one failed backup job (where `status = 'FAILED'`). Count the number of failed jobs per server.
4. For only the servers identified in step 3, process `/home/user/nosql_metrics.jsonl` (simulating a NoSQL aggregation pipeline) to calculate the total `bytes_transferred` where `type` is exactly `"backup"`.
5. Outputs a final JSON report to `/home/user/report.json` mapping the hostname to their failure count and total bytes transferred.

The format of `/home/user/report.json` must strictly be:
```json
{
  "hostname_1": {
    "failures": 2,
    "total_bytes": 5000000
  },
  "hostname_2": {
    "failures": 1,
    "total_bytes": 1048576
  }
}
```

Ensure your Python script is executable and utilizes proper parameterized queries (`?`) when interacting with SQLite to prevent injection, even though this is an internal tool. Do not hardcode the datacenter in the SQL string.