You are a Database Reliability Engineer investigating unusual backup size fluctuations. You have been given access to a SQLite database containing logs of automated backups across the fleet.

The database is located at `/home/user/backup_metadata.db`. 

Your task is to write a Python script `/home/user/analyze_backups.py` that connects to this database and performs the following operations:

1. **Reverse Engineer & Analyze**: Discover the schema of the database to understand the tables and columns storing the backup logs.
2. **Identify Anomalies (Window Functions & Aggregation)**: Write a SQL query to find "anomalous" servers. An anomalous server is one where its *most recent successful* backup size is strictly greater than 1.5 times the average size of its *last 3 successful backups* (including the most recent one).
   - Only consider backups with a 'SUCCESS' status.
   - You must use window functions to identify the most recent backups per server.
3. **Optimize (Index Strategy)**: Formulate a single `CREATE INDEX` statement that optimizes the retrieval and partitioning of the successful backups by server and time.
4. **Execution & Export**: Your Python script must:
   - Execute the `CREATE INDEX` statement on the database.
   - Run `EXPLAIN QUERY PLAN` on your anomaly detection query and save the exact output to `/home/user/plan.txt`.
   - Execute the anomaly detection query and save the results to `/home/user/anomalies.csv`. The CSV must have exactly three columns: `server_name`, `latest_size`, `avg_recent_size`. Include a header row. Round `avg_recent_size` to 2 decimal places in Python or SQL if necessary, but exact match is evaluated based on numerical equivalence.

Constraints:
- Do not modify the data in the existing tables, only add an index.
- Ensure your query uses the newly created index (the execution plan should reflect this).
- Do not install external dependencies beyond Python's standard library (e.g., `sqlite3`, `csv`).