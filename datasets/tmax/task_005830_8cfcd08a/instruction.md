You are a Database Reliability Engineer (DBRE) responsible for managing complex, interdependent backup and restoration workflows. Our multi-database architecture takes both FULL and INCREMENTAL backups, and sometimes an incremental backup of one database logically depends on a snapshot from another database to maintain referential integrity.

Your task is to write a Python script that generates a deterministic restoration plan from an SQLite metadata database.

**System State:**
An SQLite database exists at `/home/user/backup_meta.db`. 
It has two tables:
1. `backups`: 
   - `id` (INTEGER PRIMARY KEY)
   - `db_name` (TEXT)
   - `backup_type` (TEXT) - Either 'FULL' or 'INC'
   - `timestamp` (INTEGER) - Unix epoch time
   - `file_path` (TEXT) - Path to the backup file
2. `dependencies`:
   - `backup_id` (INTEGER) - The ID of the backup
   - `depends_on_id` (INTEGER) - The ID of the backup that must be restored *before* `backup_id`.

**Requirements:**
1. Create a Python script at `/home/user/generate_plan.py`.
2. The script must take two arguments: `<target_db_name>` and `<target_timestamp>`.
3. It must query `/home/user/backup_meta.db` to find the most recent backup for `<target_db_name>` where `timestamp <= <target_timestamp>`.
4. Using recursive/hierarchical queries or logic, it must resolve the entire dependency graph (all backups required to restore the target backup, including the target itself).
5. Project this dependency tree into a directed acyclic graph (DAG) to determine the restoration order. A backup can only be restored after ALL its dependencies are restored.
6. To make the sequence deterministic, sort the valid next backups by `timestamp` ascending. If timestamps are equal, sort by `id` ascending.
7. Export the materialized sequence of `file_path`s as a JSON array of strings to a file named `/home/user/restore_plan.json`.

**Example execution:**
```bash
python3 /home/user/generate_plan.py "orders_db" 1700001000
```

Please write and execute the code to generate the restoration plan for `db_alpha` at timestamp `1690000050`. The output must be written exactly to `/home/user/restore_plan.json`.