You are a Database Reliability Engineer. We have an SQLite database tracking our backup files and their dependencies at `/home/user/backups.db`. The table `backup_lineage` contains the backup hierarchy (e.g., incremental backups depending on previous backups). 

The schema is:
`CREATE TABLE backup_lineage (id TEXT PRIMARY KEY, parent_id TEXT, backup_type TEXT, file_path TEXT, timestamp DATETIME);`

We just discovered that the full backup with the ID `bkp_0001` is corrupted. Any backup that descends from this backup (directly or indirectly via `parent_id`) is also invalid and must be flagged.

Your task is to:
1. Optimize the database: The recursive queries on this table are currently slow because there is no index on the foreign key relationship. Create an appropriate index on the `backup_lineage` table to optimize queries filtering or joining by `parent_id`. Name the index `idx_parent_id`.
2. Write a Python script at `/home/user/process_lineage.py` that connects to this database and uses a Recursive Common Table Expression (CTE) to traverse the graph of dependencies.
3. The script must find the corrupted backup (`bkp_0001`) and all of its direct and indirect descendants.
4. The script must compute the `depth` of each backup in the corrupted lineage (depth 0 for `bkp_0001`, depth 1 for its immediate children, depth 2 for grandchildren, etc.).
5. Export the results to `/home/user/affected_backups.json`. The output must be a well-formatted JSON array of objects, with each object containing `id`, `file_path`, and `depth`.
6. The JSON array must be sorted by `depth` in ascending order, and then by `id` in ascending order for backups at the same depth.

Example of expected JSON format:
```json
[
  {"id": "bkp_0001", "file_path": "/backups/full/0001.tar.gz", "depth": 0},
  {"id": "bkp_0002", "file_path": "/backups/inc/0002.tar.gz", "depth": 1}
]
```

Run your Python script to generate the JSON file. Ensure both the database index and the JSON file are created successfully.