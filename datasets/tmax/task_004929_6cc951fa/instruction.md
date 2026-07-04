You are a Database Reliability Engineer (DBRE) responsible for monitoring and optimizing our backup pipeline. You have been given an SQLite database containing metadata about recent backups across multiple database clusters.

The database is located at `/home/user/backup_metadata.db`.
The database contains a single table named `backups` with the following schema:
- `id` (INTEGER PRIMARY KEY): Unique identifier for the backup.
- `cluster_id` (TEXT): The name of the database cluster.
- `type` (TEXT): The type of backup, either 'full' or 'incremental'.
- `parent_id` (INTEGER): The `id` of the backup this incremental backup depends on (NULL for full backups).
- `duration_sec` (INTEGER): Time taken to complete the backup in seconds.
- `timestamp` (DATETIME): The time the backup completed.

We need to identify performance anomalies in the backup pipeline and find the most critical backups in our dependency chains. 

Write a Python script at `/home/user/analyze_backups.py` that connects to the database and does the following:

1. **Anomaly Detection (Window Functions):**
   Using an SQL query with Window Functions, calculate the rolling average of `duration_sec` for the strictly *previous 3* backups (not including the current row) for each `cluster_id`, ordered by `timestamp`. 
   A backup is considered an anomaly if its `duration_sec` is strictly greater than `1.5` times the moving average of its previous 3 backups. (Note: Only consider rows that have at least 3 previous backups in the window to calculate the average).

2. **Dependency Graph Analytics:**
   Construct a directed graph of backup dependencies where each backup is a node, and edges go from `parent_id` to `id` (representing that `id` depends on `parent_id`). 
   Using graph analytics (you may install and use `networkx`), calculate the out-degree of all nodes. Identify the `id` of the single backup that acts as a parent to the highest number of direct child backups (the most critical backup).

3. **Output:**
   Chain these analyses together and output the results to a JSON file at `/home/user/backup_report.json` with the exact following structure:
   ```json
   {
     "critical_backup_id": <int>,
     "anomalies": [
       {
         "backup_id": <int>,
         "cluster_id": "<string>",
         "duration": <int>,
         "moving_avg": <float>
       }
     ]
   }
   ```
   *Note: If there are multiple anomalies, order them by `backup_id` ascending. Format `moving_avg` to exactly 2 decimal places (e.g., 24.33).*