You are tasked with fixing a C++ data processing pipeline that interacts with a graph-like dataset stored in SQLite. 

Currently, our pipeline reads a dependency graph of transactions using a recursive Common Table Expression (CTE) (simulating a Cypher-like graph traversal) and updates node values. However, we are facing two major issues:
1. **Deadlocks**: The multi-threaded C++ application (`/home/user/pipeline.cpp`) constantly hits `SQLITE_BUSY` deadlocks because concurrent threads attempt to read the graph and subsequently update it without proper transaction isolation/locking order.
2. **Performance**: The recursive CTE querying the `Edges` table is extremely slow due to a missing index, causing full table scans during the graph traversal.

Your objectives:
1. **Optimize the Schema**: Analyze the recursive query in `pipeline.cpp`. Create and execute a SQL script at `/home/user/optimize.sql` that adds exactly one optimal index to the `graph.db` database to fix the query plan and prevent full table scans during the recursion.
2. **Fix the Deadlock**: Modify `/home/user/pipeline.cpp` to prevent deadlocks. (Hint: SQLite's default `BEGIN` uses deferred locks. Changing the transaction strategy or locking mechanism is necessary so that read-modify-write cycles from multiple threads don't deadlock).
3. **Pipeline Output**: Update `pipeline.cpp` so that, at the very end of the `main()` function (after all threads join), it queries the final state of all nodes and writes them to `/home/user/final_nodes.csv` in the exact format: `id,value`.
4. **Build and Run**: Compile your fixed C++ application to `/home/user/pipeline` using `g++ -std=c++17 -lpthread -lsqlite3 /home/user/pipeline.cpp -o /home/user/pipeline`. Run it to ensure it completes successfully and produces the output file.

The database and starter code have been placed in `/home/user/`. 

Output constraints:
- `/home/user/optimize.sql` must contain the single `CREATE INDEX ...` statement.
- `/home/user/final_nodes.csv` must contain the CSV output, sorted by `id` ascending.