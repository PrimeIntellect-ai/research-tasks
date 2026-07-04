As a Database Reliability Engineer, you are responsible for managing backup pipelines. You need to automate the generation of backup manifests by querying a metadata database to determine which tables have changed or are affected by upstream changes.

You have a SQLite database at `/home/user/backup_meta.db` containing metadata about your tables.
The schema is:
- `tables (id INTEGER PRIMARY KEY, name TEXT, last_update INTEGER)`
- `backups (id INTEGER PRIMARY KEY, table_id INTEGER, backup_time INTEGER)`
- `dependencies (parent_id INTEGER, child_id INTEGER)`

In the `dependencies` table, `parent_id` represents the upstream table, and `child_id` represents the dependent downstream table. 

A table is considered "stale" and requires a new backup if **any** of the following conditions are met:
1. It has no records in the `backups` table.
2. Its `last_update` timestamp is strictly greater than the `backup_time` of its *most recent* backup.
3. It depends (directly or transitively) on another table that requires a backup. For example, if Table A depends on Table B, and Table B requires a backup, Table A also requires a backup.

**Your task:**
1. Write a C program at `/home/user/generate_manifest.c` that connects to the `/home/user/backup_meta.db` database.
2. Use the SQLite3 C API (`sqlite3.h`) to execute a query (using recursive CTEs or complex joins) that identifies all tables requiring a backup.
3. The C program must write the names of these tables to `/home/user/pending_backups.txt`. The table names must be sorted alphabetically, with one name per line.
4. Compile your program and run it to generate the final `/home/user/pending_backups.txt` file.

You may install any necessary C development libraries for SQLite using the system package manager.