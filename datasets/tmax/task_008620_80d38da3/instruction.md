You are a Database Reliability Engineer. We have a backup catalog stored in a SQLite database at `/home/user/backup_catalog.db`. 

The database contains a single table named `backup_jobs` with the following schema:
`CREATE TABLE backup_jobs (job_id INTEGER PRIMARY KEY, job_name TEXT, parent_job_id INTEGER, size_bytes INTEGER, status TEXT);`

Incremental backups depend on their parent backups. To restore a specific backup, we must first restore its parent, its parent's parent, and so on, back to the root full backup (which has a `parent_job_id` of NULL).

Your task:
1. Identify the full restoration chain required to restore the backup with `job_id = 73`. You must use a recursive SQL query (CTE) to trace the hierarchy from `job_id = 73` up to the root backup.
2. Export this exact restoration chain into a JSON file located at `/home/user/restore_chain.json`.
3. The JSON file must contain a single array of objects, where each object represents a backup job in the chain. The objects must have exactly two keys: `job_id` (integer) and `job_name` (string).
4. The array must be ordered chronologically by restoration sequence: the root full backup must be the first element, and `job_id = 73` must be the last element.

Write a script in your language of choice to perform this query and export the results, or use shell utilities. Ensure the final output is strictly valid JSON matching the specified schema.