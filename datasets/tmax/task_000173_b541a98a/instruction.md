You are a Database Reliability Engineer (DBRE) tasked with optimizing and extracting data from a local backup catalog database. 

We maintain an SQLite database at `/home/user/backup_catalog.db` that logs all our automated backup jobs and the files they contain. 

The database has two tables:
1. `jobs`
   - `id` (INTEGER PRIMARY KEY)
   - `type` (TEXT) - either 'full' or 'inc'
   - `status` (TEXT) - either 'success' or 'failed'
   - `start_time` (INTEGER) - unix timestamp

2. `files`
   - `id` (INTEGER PRIMARY KEY)
   - `job_id` (INTEGER) - foreign key to jobs.id
   - `size_bytes` (INTEGER)

Your objectives are:
1. **Optimize**: The database currently has no indexes other than the primary keys. Analyze the schema and queries required below, and create an appropriate index (or indexes) on the `jobs` table to optimize filtering by `status` and `type` and sorting by `start_time`.
2. **Query and Construct**: Write a script in the language of your choice to determine the correct "restore chain". The restore chain consists of:
   - The *most recent* successful 'full' backup.
   - ALL successful 'inc' (incremental) backups that occurred *after* that specific 'full' backup.
   - The sum total of `size_bytes` for all files associated with this exact restore chain (the full backup + the subsequent incremental backups).
3. **Format**: Save the result to exactly `/home/user/restore_plan.json`. It must validate against this exact JSON schema structure:
```json
{
  "full_backup_id": 10,
  "incremental_backup_ids": [12, 14],
  "total_files_size": 1048576
}
```

Constraints:
- Only successful backups should be considered. 
- You may use any language (Python, Bash+sqlite3, etc.) to perform the logic, but the final JSON file must be perfectly formatted.
- Ensure your index creation is permanently saved to the `/home/user/backup_catalog.db` file.