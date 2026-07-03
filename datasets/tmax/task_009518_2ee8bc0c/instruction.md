You are a data engineer responsible for optimizing and fixing our C-based ETL pipelines. We use SQLite for an intermediate processing step, but our pipeline workers are experiencing database deadlocks and performance issues when building graph projections.

Your task is to write a standalone C program that safely and efficiently materializes a "friend-of-a-friend" graph projection from raw relational data, using parameterized queries, optimized query plans, and concurrency-safe transactions.

**System Context & Setup:**
The raw data is located at `/home/user/etl.db`. 
It contains a table `user_connections(user_a INTEGER, user_b INTEGER)` representing direct connections. 
(Note: the database has been populated with dummy data for this task).

**Requirements:**

1. **Write the ETL script in C:**
   - Create a file `/home/user/graph_etl.c`.
   - The program should take an arbitrary number of user IDs as command-line arguments. Example: `./graph_etl 10 25 103`
   - It must connect to `/home/user/etl.db` using the SQLite3 C API.

2. **Graph Projection & Parameterization:**
   - The program must ensure a target table exists: `fof_graph(source INTEGER, target INTEGER, UNIQUE(source, target))`.
   - For *each* user ID provided via the command-line arguments, find all their "friends-of-friends" (paths of exactly length 2: the user is `user_a` in a connection to some `user_b`, and that `user_b` is `user_a` in a connection to some `user_c`. The result should be `user`, `user_c`).
   - Insert these pairs `(user, user_c)` into `fof_graph`. Ignore cases where the source equals the target (a user is a friend-of-a-friend to themselves). Ignore duplicates (handled by the UNIQUE constraint, use `INSERT OR IGNORE`).
   - **Crucial Requirement:** You *must* use a parameterized query (using `sqlite3_prepare_v2`, `sqlite3_bind_int`, etc.) for the execution to prevent SQL injection and reuse the prepared statement in the loop over the command-line arguments. Do not concatenate the user ID into the SQL string.

3. **Concurrency & Deadlock Prevention:**
   - Our ETL scheduler runs multiple instances of this program concurrently. Standard SQLite `BEGIN` statements use deferred locks, which often result in `SQLITE_BUSY` deadlocks during the read-modify-write cycle of the projection.
   - You must reverse-engineer the required locking mechanism and wrap all the inserts for a single program execution in a transaction that immediately acquires write locks to prevent deadlocks with other ETL workers.

4. **Query Optimization:**
   - The `user_connections` table currently lacks indexes, causing full table scans for the graph traversal.
   - Add a C snippet to your program (before your inserts) that creates an optimal index on `user_connections` to speed up the self-join/traversal.
   - Output the `EXPLAIN QUERY PLAN` for your core SELECT/INSERT parameterized query to `/home/user/plan.txt`. (You can do this manually in a shell script, or write it via C, as long as the file ends up correctly containing the plan showing the use of your new index).

**Build & Run Instructions:**
- Compile your program with `gcc -O2 /home/user/graph_etl.c -o /home/user/graph_etl -lsqlite3`.
- Execute your program with `./graph_etl 1 5 10` so the database is updated and ready for verification.

**Verification:**
The automated test will:
- Check that `/home/user/graph_etl.c` contains the correct transaction type to prevent SQLite upgrade deadlocks.
- Check that `/home/user/graph_etl.c` uses `sqlite3_bind_int` (or similar).
- Verify `/home/user/plan.txt` indicates the usage of an index.
- Verify the `fof_graph` table in `/home/user/etl.db` contains the mathematically correct friends-of-friends for users 1, 5, and 10 based on the raw data.