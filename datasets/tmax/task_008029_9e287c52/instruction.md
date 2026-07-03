You are a database administrator working on optimizing graph queries that run on an embedded SQLite database. 

We have a relational SQLite database located at `/home/user/graph.db` that represents a directed property graph. 
The database contains two tables:
- `nodes` (id INTEGER PRIMARY KEY, label TEXT)
- `edges` (source INTEGER, target INTEGER)

Currently, querying the graph for multi-hop paths is incredibly slow because there are no indexes on the `edges` table, and the developers are doing manual looping in application code.

Your task is to write a C++ program at `/home/user/solve.cpp` that does the following:
1. Connects to `/home/user/graph.db` using the SQLite3 C/C++ API.
2. Creates an optimal covering index on the `edges` table to drastically speed up forward graph traversals (i.e., looking up targets given a source).
3. Executes a single, optimized **Recursive CTE** (Common Table Expression) to find all distinct node IDs that are reachable from the starting node `id = 42`, up to a maximum depth of 3 hops (where depth 0 is node 42 itself, depth 1 is its direct children, etc.).
4. Writes the resulting distinct reachable node IDs (including the starting node 42) into a JSON file at `/home/user/reachable.json`. The output must be a single, strictly formatted JSON array of integers sorted in ascending order. 

Example Output format for `/home/user/reachable.json`:
```json
[42, 105, 208, 301]
```

Requirements:
- You must use C++ and the `<sqlite3.h>` library.
- Compile your program using `g++ /home/user/solve.cpp -lsqlite3 -o /home/user/solve`.
- Execute your compiled program so that it produces the `/home/user/reachable.json` file.
- The output must only contain the sorted JSON array, nothing else.

Ensure you run your program before finishing so the output file is generated.