You are a Database Reliability Engineer managing a complex backup infrastructure. Your system performs multiple types of backups (Full, Differential, and Incremental), resulting in a Directed Acyclic Graph (DAG) of backup dependencies.

You have been given a SQLite database `/home/user/backups.db` containing the metadata of all backup jobs. 

The database has two tables:
1. `backups`: 
   - `id` (INTEGER PRIMARY KEY): Unique identifier.
   - `type` (TEXT): 'FULL', 'DIFF', or 'INCR'.
   - `status` (TEXT): 'SUCCESS', 'FAILED', or 'IN_PROGRESS'.
   - `size` (INTEGER): Size of the backup in megabytes.
   - `timestamp` (INTEGER): Unix timestamp.

2. `dependencies`:
   - `parent_id` (INTEGER): ID of the backup that must be restored first.
   - `child_id` (INTEGER): ID of the dependent backup.

Due to overlapping schedules and retries, there are often multiple valid restoration paths to reach a specific backup state. 

Your task is to write a C program, `/home/user/planner.c`, that takes a target backup ID as a command-line argument and determines the optimal restoration sequence. 

The optimal sequence must:
1. Start with a 'FULL' backup.
2. End with the target backup ID.
3. Follow valid dependency edges (`parent_id` -> `child_id`).
4. **Only** use backups with a `status` of 'SUCCESS'. (This is a graph projection / filtering step).
5. Minimize the **total size** (sum of `size` of all backups in the path, including the FULL backup and the target).

Requirements for the C program:
- It must query the SQLite database using the C API (you can assume `sqlite3.h` and `libsqlite3-dev` are available).
- It must perform the graph traversal / shortest-path computation in memory or via advanced recursive SQL queries.
- It must accept the target ID as the first argument (e.g., `./planner 42`).
- It must output the sequence of backup IDs to `/home/user/restore_plan.txt`, one ID per line, starting from the FULL backup and ending with the target backup.

To complete the task:
1. Write the `/home/user/planner.c` source code.
2. Compile it using `gcc -o /home/user/planner /home/user/planner.c -lsqlite3`.
3. Run the compiled program with the target backup ID `99`. 

The final result must be the correctly populated `/home/user/restore_plan.txt` file representing the minimum-size successful restoration path.