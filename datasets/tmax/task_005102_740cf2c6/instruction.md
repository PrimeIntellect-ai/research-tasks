You are a Database Reliability Engineer investigating a cascading failure in our backup job system. The backup job metadata is stored in a SQLite database located at `/home/user/backups.db`. 

The database contains a single table:
`jobs (id TEXT PRIMARY KEY, parent_id TEXT, size_bytes INTEGER, start_time DATETIME)`

When a backup job is split into smaller chunks, it spawns child jobs (represented by `parent_id`). We need to analyze the backup lineage starting from a specific root job: `BKP-001`.

Your task is to write a Python script `/home/user/analyze_backups.py` that performs the following:

1. **Index Strategy Design**: The database currently lacks indexes for hierarchical lookups. Your script must first execute a SQL command to create an optimal index on the `jobs` table to speed up `parent_id` lookups. Name the index `idx_jobs_parent`.
2. **Recursive & Window Query**: Write and execute a single SQL query that:
   - Uses a **Recursive CTE** to find all descendants of the job `BKP-001` (including `BKP-001` itself).
   - Uses a **Window Function** to calculate the `cumulative_size_bytes` for the lineage. This should be a running total of `size_bytes` ordered by `start_time` ascending.
3. **Output Schema Validation**: Extract the results of the query and format them as a list of dictionaries. Before saving, validate the data against the following JSON Schema (you may use the `jsonschema` library, which you should install if needed):
   ```json
   {
     "type": "array",
     "items": {
       "type": "object",
       "properties": {
         "id": {"type": "string"},
         "parent_id": {"type": ["string", "null"]},
         "size_bytes": {"type": "integer"},
         "start_time": {"type": "string"},
         "cumulative_size_bytes": {"type": "integer"}
       },
       "required": ["id", "size_bytes", "start_time", "cumulative_size_bytes"]
     }
   }
   ```
4. **Output**: If the data is valid, write the JSON output to `/home/user/lineage_report.json`.

Ensure your script runs successfully and generates the correct output.