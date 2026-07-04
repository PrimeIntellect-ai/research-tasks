You are a Database Administrator working on a network telemetry analysis system. We store our network topology and bandwidth logs in an SQLite database located at `/home/user/network.db`.

Your task is to write a C program that performs an optimized data extraction pipeline. 

Requirements:
1. Write a C program at `/home/user/analyze_network.c`.
2. The program must connect to the `/home/user/network.db` SQLite3 database.
3. The program must execute a single, complex SQL query that:
   - Uses a **Recursive Common Table Expression (CTE)** to perform a graph traversal finding the shortest path (by sum of `latency`) from the node with hostname `'Gateway'` to the node with hostname `'Database'`. (Assume a directed acyclic graph for simplicity).
   - Joins the nodes along this optimal path with the `bandwidth_logs` table.
   - Uses a **Window Function** to calculate a 3-period moving average (current row, 1 preceding, 1 following) of the `bytes_transferred` for each node on the path, ordered by `timestamp`.
4. The C program must output the results into a CSV file at `/home/user/optimized_path_stats.csv`.
   - The CSV must have the header: `node_id,hostname,timestamp,smoothed_bytes`
   - `smoothed_bytes` should be formatted as a floating-point number with exactly 2 decimal places.
   - Rows should be ordered by the path sequence (from Gateway to Database), and then by `timestamp` ascending.

Database Schema Details (already existing):
- `nodes(id INTEGER PRIMARY KEY, hostname TEXT)`
- `edges(source_id INTEGER, target_id INTEGER, latency INTEGER)`
- `bandwidth_logs(node_id INTEGER, timestamp DATETIME, bytes_transferred INTEGER)`

Note: You will need to ensure `libsqlite3-dev` is installed to compile your C program. Compile your program to `/home/user/analyze_network` and execute it to generate the CSV.