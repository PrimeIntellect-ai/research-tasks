You are a database reliability engineer managing backups for a critical system. The backup metadata is stored in an SQLite database at `/home/user/backups.db`. 

The database contains two tables:
1. `backups`: `id` (INTEGER PRIMARY KEY), `name` (TEXT), `size_mb` (INTEGER)
2. `dependencies`: `id` (INTEGER), `parent_id` (INTEGER)

Incremental backups depend on previous backups. To restore an incremental backup, you must restore it and all of its ancestors up to the root (full backup). The `dependencies` table maps a backup `id` to its immediate `parent_id`.

Your task:
1. Write a C++ program at `/home/user/calc_restore_size.cpp` that connects to `/home/user/backups.db`.
2. The program should accept a backup `name` as a command-line argument.
3. Using the SQLite3 C++ API, construct a parameterized recursive query (CTE) to find the total size in MB required to restore the given backup name (i.e., the sum of `size_mb` for the backup itself and all its recursive ancestors).
4. The program should print exactly the integer sum to standard output.
5. Compile your C++ program (make sure to link the `sqlite3` library).
6. Read the file `/home/user/targets.txt`, which contains a list of backup names (one per line). For each name, execute your C++ program and save the results in `/home/user/restore_report.txt`.

The format of `/home/user/restore_report.txt` must be exactly:
`[BackupName]: [TotalSize] MB`
(e.g., `Inc_A2: 1150 MB`)

Ensure your C++ code securely handles the parameter injection using prepared statements.