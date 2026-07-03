You are a data engineer managing an ETL pipeline. The execution network and historical job latencies are stored in an SQLite database. You need to write a C++ program to analyze this data, find the most efficient execution path, and export the result.

The database is located at `/home/user/etl_graph.db` and contains two tables:
1. `nodes`: `(id INTEGER PRIMARY KEY, name TEXT)`
2. `edges`: `(source INTEGER, target INTEGER, latency INTEGER, created_at INTEGER)`

Due to a bug in the pipeline logger, the `edges` table contains stale rows. Multiple latency records exist for the same `(source, target)` pairs. 

Your tasks are:
1. Write a C++ program in `/home/user/optimizer.cpp` that connects to the SQLite database. You will likely need to install the SQLite development libraries.
2. Query the database to retrieve the graph. You must perform cross-query aggregation (or write a summarization SQL query in your code) to resolve the stale rows: for any `(source, target)` pair, only use the `latency` from the row with the maximum `created_at` timestamp.
3. Using the cleansed data, implement a graph traversal algorithm to compute the shortest path (minimum total latency) from the node named `'Extract'` to the node named `'Load'`.
4. Export the final computed path and its aggregated latency to a JSON file at `/home/user/shortest_path.json`.

The JSON file must precisely follow this exact format (no extra whitespace or line breaks):
`{"path":["Extract","NodeX","NodeY","Load"],"total_latency":42}`

Requirements:
- Do not use any external C++ libraries for graph traversal or JSON generation (standard library only). You may use `<sqlite3.h>` for database access.
- Ensure your C++ program compiles and runs successfully.