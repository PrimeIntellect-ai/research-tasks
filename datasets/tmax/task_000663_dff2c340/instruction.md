You are a Database Reliability Engineer (DBRE) tasked with managing and restoring databases from complex backup chains. A critical failure has occurred on the `auth_prod` database, and you need to determine the exact sequence of backups to restore to recover the system to the latest possible state right before the crash.

The crash occurred at precisely `'2023-10-27 14:00:00'`.

You have a SQLite database at `/home/user/backup_catalog.db` that contains the metadata for all backup jobs across the cluster. The database has a single table:
`backups(id TEXT PRIMARY KEY, db_name TEXT, backup_type TEXT, parent_id TEXT, timestamp TEXT, size_mb INTEGER, duration_sec INTEGER)`

A valid restoration chain always starts with a `FULL` backup and follows a sequence of `INC` (incremental) backups linked by the `parent_id` field (where an incremental backup's `parent_id` points to the `id` of the preceding backup in the chain). 

Your task is to write a Python script that:
1. Uses a recursive SQL query (CTE) to traverse the backup hierarchy and identify the correct restoration chain for `auth_prod`.
2. Filters the chain so that it only includes backups completed *before* the crash timestamp (`2023-10-27 14:00:00`).
3. Selects the single chain that gets the database as close to the crash time as possible.
4. Calculates the `total_size_mb` and `total_duration_sec` for this entire chain.
5. Projects the result into a JSON file located at `/home/user/restore_plan.json`.

The JSON file must have exactly this structure:
```json
{
  "db_name": "auth_prod",
  "target_time": "2023-10-27 14:00:00",
  "chain": ["id_of_full_backup", "id_of_inc_1", "id_of_inc_2", "..."],
  "total_size_mb": 1234,
  "total_duration_sec": 567
}
```
*Note: The `chain` array must be ordered chronologically from the FULL backup to the final incremental backup.*