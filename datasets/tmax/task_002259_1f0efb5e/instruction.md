You are a Database Reliability Engineer (DBRE) responsible for the backup infrastructure. We track the complex dependencies of our backup jobs (databases, tables, views, and export tasks) as a directed graph stored in an SQLite database. 

Recently, our primary sales database backup failed. We need to identify all downstream backup jobs that also failed so we can trigger targeted retries, rather than a full system retry. 

The database is located at `/home/user/backup_metadata.db` and contains three tables:
1. `nodes` (id INTEGER PRIMARY KEY, name TEXT, type TEXT)
2. `edges` (source_id INTEGER, target_id INTEGER) - Represents a dependency where `target_id` strictly depends on the completion of `source_id`.
3. `backup_runs` (id INTEGER PRIMARY KEY, node_id INTEGER, run_time DATETIME, status TEXT) - Logs of every backup task execution.

Your task is to:
1. **Optimize the database**: The database is currently missing indexes, making graph traversals and temporal queries very slow in production. Design and create the necessary indexes on the `edges` and `backup_runs` tables to optimize recursive graph traversal and fetching the latest run status for a node.
2. **Graph Projection & Querying**: Write a Python script at `/home/user/analyze_failures.py`. This script must:
   - Connect to `/home/user/backup_metadata.db`.
   - Use a recursive CTE (Common Table Expression) OR an in-memory graph projection (like NetworkX) to find all nodes that transitively depend on the node named `db_sales` (i.e., all nodes reachable from `db_sales` traversing from `source_id` to `target_id`).
   - For each dependent node, determine its *most recent* backup status (based on the maximum `run_time` in `backup_runs`).
   - Filter this list to include ONLY the nodes whose most recent backup status is exactly `'FAILED'`.
3. **Output**: The Python script must output a JSON-formatted list of the names of these failed dependent nodes, sorted alphabetically, to `/home/user/failed_downstream.json`.

Ensure your Python script is executable and runs successfully.