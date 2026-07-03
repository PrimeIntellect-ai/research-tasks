You are a Database Reliability Engineer managing backup systems. A central SQLite database at `/home/user/backups.db` stores metadata about all database backups, including hierarchical dependencies (e.g., incremental backups depending on previous backups). 

You need to write a Python script (`/home/user/analyze_backups.py`) to generate a restoration plan for the `prod_payments` database.

The `backup_catalog` table has the following schema:
- `id` (INTEGER PRIMARY KEY)
- `db_name` (TEXT)
- `backup_type` (TEXT): 'FULL' or 'INC'
- `parent_id` (INTEGER): The ID of the backup this backup depends on (NULL for FULL backups)
- `size_bytes` (INTEGER)
- `timestamp` (DATETIME)

Your script must:
1. Use a **recursive query (CTE)** to trace the backup dependency chain for the `prod_payments` database, starting *only* from the **most recent** 'FULL' backup.
2. Include all subsequent 'INC' (incremental) backups that are descendants of this specific FULL backup.
3. Use a **window function** within the SQL query (or in Python if chained) to calculate the `cumulative_size_bytes` of the restoration chain at each step, ordered by `timestamp` ascending.
4. Validate the extracted restoration plan data against the exact JSON schema provided below.
5. Save the valid JSON array to `/home/user/restoration_plan.json`.

Expected JSON Output Schema (it must be an array of objects matching this):
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "backup_id": { "type": "integer" },
      "backup_type": { "type": "string" },
      "size_bytes": { "type": "integer" },
      "cumulative_size_bytes": { "type": "integer" }
    },
    "required": ["backup_id", "backup_type", "size_bytes", "cumulative_size_bytes"]
  }
}
```

The final output file `/home/user/restoration_plan.json` must strictly contain only the JSON array containing the chain starting from the most recent full backup.