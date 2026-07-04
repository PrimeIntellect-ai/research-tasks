You are a Database Reliability Engineer (DBRE) tasked with managing a complex system of incremental backups. We have an SQLite database at `/home/user/backups.db` containing metadata about our backups, which are structured as a graph (each incremental backup depends on a parent backup, ultimately tracing back to a base 'full' backup).

Your task is to write a C program that calculates the restoration plan for a given backup ID.

1. **Reverse Engineer the Data Model**: Examine the SQLite database at `/home/user/backups.db` to understand how the backups and their dependencies (lineage) are stored. The database lacks foreign keys or clear documentation, so you must figure out the schema.
2. **Write the Planner Tool**: Create a C program at `/home/user/planner.c` that takes a target backup ID as its first command-line argument. It should connect to `/home/user/backups.db` using the SQLite3 C API.
3. **Graph Projection via SQL**: Your C program must execute a query (ideally using a Recursive CTE) that starts from the target backup ID, traverses up the dependency graph to find the root ('full' backup), and calculates the sequence of backups needed to restore the target.
4. **Calculate Metrics**: Determine the total size (in bytes) of all the backups in the restoration path.
5. **Output Format**: Your C program must print the restoration path from the root to the target, followed by the total size. Example output format:
   ```
   Path: b1 -> b2 -> b3 -> b4
   Total Size: 10850
   ```
6. **Query Plan Optimization**: The current database is unindexed and queries could be slow on a large dataset. Identify the optimal index(es) needed to speed up the parent lookup traversal. Write the SQL `CREATE INDEX` statement(s) into a file named `/home/user/optimize.sql`.

Compile your C program to an executable named `/home/user/planner` (e.g., `gcc /home/user/planner.c -o /home/user/planner -lsqlite3`). Ensure your program works correctly when we run `/home/user/planner <backup_id>`.