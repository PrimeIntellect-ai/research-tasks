You are a Database Reliability Engineer investigating a set of backup metadata. Recently, a deadlock between concurrent backup registration transactions resulted in some fragmented backup chains. 

You need to analyze the current backup dependency tree stored in a SQLite database located at `/home/user/backups.db`. 

The database has a single table:
`CREATE TABLE backups (backup_id INTEGER PRIMARY KEY, parent_id INTEGER, size_bytes INTEGER, job_name TEXT);`
*(Note: `parent_id` is the `backup_id` of the backup that the current incremental backup is based on. Root backups have a `parent_id` of NULL).*

Write a Python script at `/home/user/analyze_backups.py` that connects to this database and performs the following analysis:

1. **Recursive Chain Aggregation:** Using a single recursive SQL query (CTE), calculate the total `size_bytes` of the entire backup chain originating from `backup_id = 1`. This includes backup 1 and all of its direct and indirect descendants.
2. **Window Function Analysis:** Using a single SQL query with a window function, determine the `backup_id` of the largest backup (by `size_bytes`) for each distinct `job_name`. If there is a tie, pick the one with the highest `backup_id`.

Your Python script must execute these queries and output the results into a JSON file at `/home/user/summary.json` with the exact following structure:

```json
{
  "chain_1_total_size": <integer_total_size>,
  "largest_per_job": {
    "<job_name_1>": <integer_backup_id>,
    "<job_name_2>": <integer_backup_id>
  }
}
```

Constraints:
- You must use the `sqlite3` standard library in Python.
- Do not install any external Python packages (e.g., pandas or SQLAlchemy).
- The JSON file must be properly formatted. 
- Execute your script so that `/home/user/summary.json` is generated.