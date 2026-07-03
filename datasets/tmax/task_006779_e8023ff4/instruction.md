You are a Database Reliability Engineer managing backup metadata across hundreds of database servers. The metadata is stored in a SQLite3 database located at `/home/user/backups.db`.

Your task is to analyze the backup chains to determine the exact storage required to restore a specific server to its most recent state. Backups are hierarchical: an Incremental (I) depends on a previous Incremental or Full (F) backup, and Differential (D) depends on a Full backup. The chain is linked via the `parent_id` column.

Database Schema for `/home/user/backups.db`:
- `servers` (id INTEGER PRIMARY KEY, hostname TEXT)
- `backups` (id INTEGER PRIMARY KEY, server_id INTEGER, parent_id INTEGER, type TEXT, size_bytes INTEGER, created_at DATETIME)

Perform the following steps:

1. **Optimize the Database**: Write and execute a SQL script to create indexes on the `backups` table that optimally support querying the latest backup per server and recursively traversing the `parent_id` chain. Save your index creation statements in `/home/user/indexes.sql`.

2. **Write a C Program**: Create a C program at `/home/user/analyze_restore.c` that connects to `/home/user/backups.db` using the `sqlite3` C library.
    - The program must use a **Recursive CTE** to find the most recent backup (by `created_at`) for the server with hostname `db-master-42`, and traverse upwards through its `parent_id` chain until it reaches the root Full ('F') backup.
    - Calculate the total number of backups in this specific restore chain (Chain Length) and the sum of `size_bytes` of all backups in this chain (Total Size).
    - The program must output the result to a file exactly at `/home/user/restore_report.txt` in the following exact format:
      `Server: db-master-42 | Chain Length: <L> | Total Size: <S> bytes`

3. **Compile and Run**: Compile your C program to an executable named `/home/user/analyze_restore` (link against `-lsqlite3`) and run it to produce the report.

Notes:
- You may need to install the SQLite3 development headers and compiler tools (`sudo apt-get update && sudo apt-get install -y build-essential libsqlite3-dev sqlite3`).
- Ensure `/home/user/restore_report.txt` contains only the single line requested.