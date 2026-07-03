You are a Database Reliability Engineer managing backups for a custom graph database system built on top of SQLite. 

Recently, concurrent backup and restore operations have been deadlocking, and query performance on deep graph traversals is degrading. You need to write a C++ diagnostic tool that replicates the issue, optimizes the graph queries, and demonstrates a deadlock scenario.

Write a C++ program at `/home/user/graph_diag.cpp` that does the following:

1. **Database Setup & Index Strategy:**
   - Opens (or creates) an SQLite database at `/home/user/graph.db`.
   - Creates a `nodes` table: `id TEXT PRIMARY KEY, props TEXT`.
   - Creates an `edges` table: `source TEXT, target TEXT, rel_type TEXT`.
   - Creates a composite index named `idx_graph_traversal` to optimize forward graph traversals (finding targets given a source).

2. **Parameterized Data Insertion:**
   - Uses C++ `sqlite3_prepare_v2` and `sqlite3_bind_*` functions (parameterized queries) to safely insert the following graph:
     - Nodes: 'A', 'B', 'C', 'D'
     - Edges: A->B, B->C, C->D, A->D (all with rel_type 'DEPENDS_ON')

3. **Graph Query Construction (Cypher to SQL CTE):**
   - Write a parameterized Recursive CTE in SQL that simulates the Cypher query: 
     `MATCH (n {id: $start_node})-[*]->(m) RETURN m.id`
   - Execute this query starting from node 'A'.
   - Write the resulting reachable node IDs (in any order) to `/home/user/traversal.log`, one ID per line.

4. **Deadlock Simulation:**
   - Create two concurrent `std::thread`s to simulate the flawed backup/restore processes.
   - **Thread 1 (Backup):** Begins a transaction, updates `props` for node 'A', sleeps for 500 milliseconds, then tries to update `rel_type` for edge A->B.
   - **Thread 2 (Restore):** Begins a transaction, updates `rel_type` for edge A->B, sleeps for 500 milliseconds, then tries to update `props` for node 'A'.
   - Since SQLite locks the whole database, concurrent writes will result in a `SQLITE_BUSY` error. Catch this error in either thread.
   - If a `SQLITE_BUSY` (or deadlock equivalent) is caught, write the exact string `DEADLOCK_DETECTED` to `/home/user/deadlock.log`.

Compile your code using standard C++11 or higher (e.g., `g++ -std=c++11 -pthread graph_diag.cpp -lsqlite3 -o graph_diag`) and execute it. 

Ensure that:
- You never use string concatenation for values in your `INSERT` or CTE queries.
- The compiled executable `/home/user/graph_diag` successfully runs and generates `graph.db`, `traversal.log`, and `deadlock.log`.