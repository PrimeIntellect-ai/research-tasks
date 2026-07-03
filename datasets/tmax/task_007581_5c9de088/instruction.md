You are a Database Reliability Engineer investigating a backup replication issue. Our master SQLite database tracking backup nodes (`/home/user/backups.db`) is experiencing severe query performance degradation during recovery path calculations, and we suspect suboptimal indexing. 

Additionally, the recovery path calculation tool written in C (`/home/user/recovery.c`) is incomplete and currently vulnerable to SQL injection, as it relies on string formatting instead of parameterized queries.

Your task is to fix the database and complete the C program to successfully compute the shortest recovery path.

**Step 1: Database Optimization**
The `/home/user/backups.db` database contains two tables: `nodes(id TEXT PRIMARY KEY)` and `edges(source TEXT, target TEXT, weight INTEGER)`. 
There is an existing index `idx_edges_bad` on the `edges` table that is inefficient for our graph traversal. 
- Connect to the SQLite database and `DROP` the `idx_edges_bad` index.
- Create a new covering index named `idx_edges_cov` on the `edges` table that indexes `source`, `target`, and `weight` (in that order) to optimize the query plan for the C program.

**Step 2: Complete the C Application**
The file `/home/user/recovery.c` contains a skeleton for Dijkstra's algorithm. 
- Implement the `get_edges` function inside the C file. 
- Your implementation MUST use SQLite parameterized queries (`sqlite3_prepare_v2`, `sqlite3_bind_text`, `sqlite3_step`, etc.) to fetch all outgoing edges for a given `source` node.
- Do not use `sprintf` or string concatenation to build the query.
- Compile the program: `gcc /home/user/recovery.c -lsqlite3 -o /home/user/recovery`

**Step 3: Execute and Output**
- Run your compiled program to find the shortest recovery path from node `Start` to node `Recovery`.
- The program should output the sequence of nodes in the shortest path, separated by `->` (e.g., `Start->Node1->Node2->Recovery`), followed by a newline.
- Save exactly this output to `/home/user/recovery_path.txt`.

Ensure your C code gracefully handles SQLite errors and correctly frees resources (`sqlite3_finalize`).