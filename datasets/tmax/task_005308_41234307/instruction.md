You are a Database Reliability Engineer managing backup lineage for a large system. You have a SQLite database `/home/user/backups.db` containing a table `backup_lineage` that tracks full and incremental backups.

Table schema:
`CREATE TABLE backup_lineage (id INTEGER PRIMARY KEY, parent_id INTEGER, type TEXT, size INTEGER);`

There is a Python script at `/home/user/export_lineage.py` that is supposed to take a backup ID as an argument, recursively find all dependent incremental backups (the knowledge graph of the backup lineage), and export the result as JSON. 

However, the script has two issues:
1. **Wrong Results / Explosion:** The recursive CTE inside the script is generating incorrect results because of an implicit cross join (or incorrect join condition) in the recursive step. It joins on `type` instead of properly linking the child's `parent_id` to the parent's `id`.
2. **Missing Index:** The query is unoptimized. 

Your task:
1. Fix the recursive CTE in `/home/user/export_lineage.py` so that it correctly traverses the hierarchy (child `parent_id` matches the parent `id`).
2. Update the Python script to execute a command that creates an index named `idx_parent` on the `parent_id` column of the `backup_lineage` table *before* running the SELECT query.
3. Run the script for backup ID `1` and redirect its output to `/home/user/lineage_1.json`.

The final output in `/home/user/lineage_1.json` must be a valid JSON array of objects, containing the exact hierarchy for backup ID 1.