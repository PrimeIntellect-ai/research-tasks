You are a data engineer building an ETL pipeline using C++ and SQLite. You are working with an existing database at `/home/user/graph.db` that contains graph data in two tables:
- `nodes(id INTEGER PRIMARY KEY, name TEXT)`
- `edges(src INTEGER, dst INTEGER, weight REAL)`

Your task is to write a C++ program at `/home/user/pipeline.cpp` that performs a series of database operations, analytical queries, and concurrent transaction testing. 

Write the C++ program to do the following in order:
1. **Index Strategy Design**: Connect to `/home/user/graph.db` and create a composite index named `idx_edges_src_dst` on the `edges` table covering `src` and `dst` to optimize future graph query operations.
2. **Parameterized Query Construction**: Use a prepared statement with parameterized bindings to safely insert a new edge into the `edges` table: `src = 100`, `dst = 200`, `weight = 1.5`.
3. **Analytical Aggregation**: Execute a SQL query utilizing Window Functions to calculate the `DENSE_RANK()` of all destination nodes (`dst`) based on their total incoming weight (`SUM(weight)`), ordered descending. Find the newly calculated dense rank of node `200`. Write this single integer rank to the file `/home/user/rank.txt`.
4. **Transaction Deadlock Simulation**: To test pipeline resilience, purposefully trigger an `SQLITE_BUSY` error. Spawn two concurrent threads, each opening its own connection to `/home/user/graph.db`. 
   - Thread A: Execute `BEGIN;`, `SELECT COUNT(*) FROM edges;`, sleep for 200ms, then attempt to `UPDATE edges SET weight = weight + 0.1 WHERE src = 100;`.
   - Thread B: Sleep for 50ms, execute `BEGIN;`, `SELECT COUNT(*) FROM edges;`, then attempt to `UPDATE edges SET weight = weight + 0.2 WHERE src = 200;`.
   - One of these updates will fail because SQLite cannot upgrade the read lock to a write lock while the other connection holds a read lock (a classic deadlock scenario causing a busy timeout). Catch the exact SQLite error code returned (which should be the integer for `SQLITE_BUSY`) and write this integer to `/home/user/error.txt`.

Ensure your C++ code includes necessary headers (`<sqlite3.h>`, `<thread>`, `<chrono>`, etc.) and cleans up resources properly. Provide a bash script `/home/user/run.sh` that compiles your C++ program (linking `sqlite3` and `pthread`) and runs it. 

After you write the files, execute `/home/user/run.sh` to ensure it works and produces `/home/user/rank.txt` and `/home/user/error.txt`.