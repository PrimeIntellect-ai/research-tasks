You are a Database Reliability Engineer (DBRE) tasked with planning the restoration of a microservice architecture from a backup. 

You have been provided with an SQLite database at `/home/user/backups.db` containing server backup metadata and their dependencies. 
However, there is a known issue: the index `idx_active` on the `dependencies` table is corrupted and frequently returns stale, deleted rows for queries filtering by `is_active = 1`.

Your task is to write a Python script that processes this data to determine the restoration priority of each server.

You must do the following:
1. Query the `/home/user/backups.db` database for all servers and active dependencies. You **must** bypass the corrupted index (e.g., using SQLite's `NOT INDEXED` clause) to ensure you only retrieve rows where `is_active = 1`.
2. Build a directed graph of the active dependencies (where a source server depends on a target server).
3. Compute the **in-degree centrality** of each server in this active dependency graph using the `networkx` library.
4. Calculate the `total_backup_size` for each server. This is defined as the server's own `size_gb` plus the `size_gb` of all immediate target servers it directly depends on.
5. Output the results to `/home/user/restore_priority.json`.

The output must be a JSON array of objects, sorted by `in_degree_centrality` descending, and then by `total_backup_size` descending.
Each object should have the exact following format:
```json
[
  {
    "server_name": "DB-01",
    "in_degree_centrality": 0.5,
    "total_backup_size": 500
  }
]
```

Ensure your script handles the cross-query aggregation efficiently and produces the exact JSON structure requested.