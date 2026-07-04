You are an AI assistant helping a dataset researcher process a graph database. 

The researcher has an SQLite database located at `/home/user/dataset.db` that contains a knowledge graph. The schema has two tables:
- `nodes` (id INTEGER PRIMARY KEY, label TEXT)
- `edges` (source INTEGER, target INTEGER, weight INTEGER)

Recently, the database suffered an abrupt power loss. The researcher suspects that the index on the `edges` table (named `idx_edges_source_target`) is corrupted and returning stale/ghost rows when standard queries are executed. 

Your task is to write a C program at `/home/user/process_graph.c` that bypasses this corrupted index, extracts the graph, finds specific patterns, and aggregates the results.

Requirements for the C program:
1. Connect to `/home/user/dataset.db` using the SQLite C API (`sqlite3.h`).
2. Query the `edges` table using the `NOT INDEXED` clause (e.g., `FROM edges NOT INDEXED`) to ensure you are doing a full table scan and bypassing the corrupted index. Also fetch the `nodes`.
3. Find all "heavy triangles" in the graph. A triangle is defined as a cycle of exactly 3 distinct nodes (A -> B -> C -> A). A "heavy" triangle is one where the sum of the weights of its three edges is strictly greater than 100.
4. For every unique node that is part of *at least one* heavy triangle, calculate its true `out_degree` (the total number of outgoing edges from that node, calculated over the entire uncorrupted graph using `NOT INDEXED`).
5. Export the final aggregated results to `/home/user/heavy_triangles.csv`.
6. The CSV must have the header `node_id,label,out_degree` and be sorted in ascending order by `node_id`.

You may need to install the SQLite3 development libraries to compile your code. You can use `sudo apt-get update && sudo apt-get install -y libsqlite3-dev`. Compile your code with `gcc -o process_graph process_graph.c -lsqlite3`. Run your executable to generate the required CSV.