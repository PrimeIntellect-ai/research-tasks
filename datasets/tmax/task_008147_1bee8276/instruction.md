You are a Database Reliability Engineer investigating a concurrent scheduling deadlock that corrupted several recent incremental backups. To restore the system, you must trace the backup dependency graph to find the shortest valid path from the corrupted backup back to a safe "base" backup.

You have been provided a SQLite3 database at `/home/user/backups.db` which contains the metadata of all backup jobs. 

The database has two tables:
1. `backups`
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `is_base_backup` (INTEGER) - 1 if it is a full base backup, 0 if incremental.

2. `deps`
   - `backup_id` (INTEGER)
   - `depends_on` (INTEGER) - represents a directed edge meaning `backup_id` requires `depends_on` to be restored first.

Your task is to write a C program that connects to this SQLite3 database, queries it, and calculates the shortest restoration path from backup ID `42` to *any* base backup (`is_base_backup = 1`).

Requirements:
1. Write your C code in `/home/user/find_restore_path.c`.
2. Use the SQLite3 C API (`sqlite3.h`). You may need to install the development headers (`sudo apt-get update && sudo apt-get install -y libsqlite3-dev` if not present) and link with `-lsqlite3`.
3. You must use a single complex SQL query (e.g., a Recursive CTE) executed from your C program to compute the shortest path, rather than dumping the whole graph into memory.
4. Your C program must print the shortest path strictly in the following format to standard output:
   `RESTORE_PATH: 42 -> A -> B -> C` (where C is the ID of the base backup).
5. Compile your program to `/home/user/find_restore_path`.
6. Run your program and redirect its output to `/home/user/path_output.txt`.

Ensure the output exactly matches the requested schema so our automated verification systems can parse it.