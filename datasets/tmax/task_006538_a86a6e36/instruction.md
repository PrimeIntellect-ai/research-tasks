You are a Database Reliability Engineer managing a complex backup catalog for a fleet of databases. All backup metadata is stored in a local SQLite database located at `/home/user/backups.db`. 

The database contains a single table:
`backup_jobs(id INTEGER PRIMARY KEY, db_name TEXT, start_time DATETIME, size_bytes INTEGER, parent_backup_id INTEGER, status TEXT)`

Full backups have `parent_backup_id IS NULL`. Incremental backups have a `parent_backup_id` pointing to the previous backup in the chain (which could be a full backup or another incremental backup). 

Your task is to write a Python script at `/home/user/analyze_backups.py` that performs the following tasks:

1. **Index Strategy Design**: Before running the heavy analysis, your script must execute SQL statements to create optimal indexes on the `backup_jobs` table to speed up recursive hierarchical queries (by parent ID) and window functions (partitioned by database name and ordered by start time).
2. **Recursive and Hierarchical Query**: Write a query using a Recursive CTE to calculate the `total_chain_size` for every full backup. A backup chain consists of a full backup and ALL its descendant incremental backups.
3. **Window Functions**: Using the aggregated chain sizes, apply a window function to determine if a backup chain is "anomalous". A chain is anomalous (`is_anomalous = True`) if its `total_chain_size` is strictly greater than 1.5 times the average `total_chain_size` of the *previous two* backup chains for the same `db_name` (ordered by the full backup's `start_time`). If there are fewer than two previous chains, `is_anomalous` should be `False` (or 0).
4. **Output Schema Validation**: Your Python script must extract the results: `root_backup_id` (the ID of the full backup), `db_name`, `total_chain_size`, and `is_anomalous` (boolean). It must validate this output against a formal JSON schema using the Python `jsonschema` library, and then write the valid JSON array to `/home/user/analysis_results.json`.

The required JSON schema for validation is:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "root_backup_id": {"type": "integer"},
      "db_name": {"type": "string"},
      "total_chain_size": {"type": "integer"},
      "is_anomalous": {"type": "boolean"}
    },
    "required": ["root_backup_id", "db_name", "total_chain_size", "is_anomalous"]
  }
}
```

Ensure your script handles all operations (indexing, querying, validation, and file writing) autonomously when executed via `python3 /home/user/analyze_backups.py`.