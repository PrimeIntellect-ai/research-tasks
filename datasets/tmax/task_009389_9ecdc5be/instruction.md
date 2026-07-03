You are a Database Reliability Engineer (DBRE) managing a complex backup system. The metadata for all backup jobs and their restoration dependency chains is stored in a local SQLite database at `/home/user/backup_metadata.db`.

Your task is to:
1. Analyze the schema of `/home/user/backup_metadata.db` to understand how backups and their dependency relationships (directed edges from a required parent backup to a child backup) are stored.
2. Write a C program at `/home/user/get_restore_chain.c` that uses the `sqlite3` C library to perform a graph traversal. 
3. The C program must accept exactly one command-line argument: the name of a target backup.
4. Using parameterized queries (e.g., `sqlite3_prepare_v2` and `sqlite3_bind_text`) to prevent SQL injection, the program must find the shortest restoration path (fewest hops) from the foundational root backup, which is always named `full_base_001`, to the target backup specified by the command-line argument. You may use a Recursive CTE or iterative graph traversal in your C code.
5. The program must export the result as a single comma-separated line of backup names, ordered from `full_base_001` to the target backup, and write it to `/home/user/restore_plan.csv`.
6. Compile your program to `/home/user/get_restore_chain` (ensure you link the sqlite3 library).
7. Execute your program with the target backup name: `incr_log_999`.

Ensure your program handles errors gracefully. You may need to install the SQLite3 development headers to compile your C program.