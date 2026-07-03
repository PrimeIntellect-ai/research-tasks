You are a Database Reliability Engineer (DBRE) tasked with automating the generation of backup restore plans. You have an SQLite database containing metadata about all system backups, which form a dependency graph (incremental backups depend on previous backups, tracing back to a full backup).

The database is located at `/home/user/backup_metadata.db` and has the following table:
`backups(id TEXT PRIMARY KEY, type TEXT, timestamp DATETIME, size_mb INTEGER, parent_id TEXT)`
- `type` is either 'FULL' or 'INCREMENTAL'.
- `parent_id` points to the `id` of the backup this backup depends on (NULL for 'FULL' backups).

Your task is to write a Python script `/home/user/generate_plan.py` that takes a single target timestamp as a command-line argument (format: `YYYY-MM-DD HH:MM:SS`).

The script must:
1. Connect to the SQLite database.
2. Use parameterized queries to securely pass the target timestamp.
3. Identify the most recent backup (of any type) that occurred AT OR BEFORE the target timestamp.
4. Traverse the dependency graph (using a recursive query or graph traversal pattern) backwards from this backup to its root 'FULL' backup.
5. Use a SQL Window Function to calculate the cumulative total size of the backups in the exact order they need to be restored (from FULL to the final INCREMENTAL).
6. Write the resulting restore plan to `/home/user/restore_plan.csv`.

The output CSV file must have exactly this header: `step_number,backup_id,cumulative_size_mb`.
`step_number` should start at 1 for the FULL backup and increment by 1 for each subsequent incremental backup.

After writing the script, run it using the target timestamp: `"2023-11-05 14:30:00"`.