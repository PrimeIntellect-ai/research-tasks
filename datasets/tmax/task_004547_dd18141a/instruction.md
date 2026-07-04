You are a Database Reliability Engineer tasked with analyzing and optimizing a backup orchestration system. The system's job dependencies are exported as a JSON graph, while the backup run logs and NoSQL-style configuration documents are stored in an SQLite database. 

Your goal is to find the critical execution path, extract specific NoSQL document attributes, calculate performance metrics using window functions, and optimize the database for these analytical queries.

**Files provided:**
1. `/home/user/job_graph.json`: A directed graph of backup job dependencies represented as an adjacency list mapping a job ID to a list of job IDs that depend on it.
2. `/home/user/backups.db`: An SQLite database with the following schema:
   - `backup_logs` (id INTEGER PRIMARY KEY, job_id TEXT, run_date TEXT, duration_seconds INTEGER)
   - `job_configs` (job_id TEXT PRIMARY KEY, config_json TEXT)

**Tasks:**
1. **Graph Traversal**: Write a Python script `/home/user/analyze.py` that reads `/home/user/job_graph.json` and finds the shortest path (fewest edges) from `"JOB_START"` to `"JOB_END"`.
2. **Data Querying & Cross-Representation Mapping**: For each job in the shortest path (in order from start to end), query the SQLite database to:
   - Extract the `storage_target` value from the `config_json` field in the `job_configs` table (using SQLite's built-in JSON functions).
   - Calculate the 3-run moving average of `duration_seconds` for that job. This must be done inside the database using SQL Window Functions (`AVG()` over the current row and 2 preceding rows, partitioned by `job_id` and ordered by `run_date` ascending). You need the moving average value corresponding to the *latest* `run_date` for that job.
3. **Report Generation**: Output the aggregated results to `/home/user/report.json` as a JSON array of objects, preserving the path order. The objects must have this exact structure:
   ```json
   [
     {
       "job_id": "JOB_START",
       "storage_target": "s3",
       "latest_3run_avg": 125.5
     },
     ...
   ]
   ```
4. **Index Strategy Design**: The `backup_logs` table contains millions of rows, making your window function query slow. Design the optimal index(es) to support your exact analytical query (partitioning and sorting) and write the `CREATE INDEX` statement(s) to a file named `/home/user/optimize.sql`. Do not execute this SQL script, just create the file.

Make sure your Python script runs flawlessly and generates the correct `report.json`.