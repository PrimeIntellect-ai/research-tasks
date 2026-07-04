You are a Database Reliability Engineer (DBRE) tasked with querying a restored graph database backup that has partial corruption. 

We have an SQLite database backup located at `/home/user/routing.db`. This database represents a network routing graph and contains a single table:
`routes (src INTEGER, dst INTEGER)`

An index was created on this table: `CREATE INDEX idx_src ON routes(src);`

During the backup restoration, we discovered that the `idx_src` index is corrupted for a specific set of nodes. For these corrupted nodes, the index points to stale (previously deleted) phantom edges. Normal queries like `SELECT count(*) FROM routes WHERE src = ?` will return incorrect, inflated counts for these specific nodes because SQLite uses the corrupted index.

Fortunately, we have a screenshot of the corrupted node IDs identified by the storage team before the system went down. This image is located at `/app/corrupted_nodes.png`. 

Your task is to:
1. Extract the list of corrupted node IDs from the image `/app/corrupted_nodes.png` (you can use `tesseract`).
2. Write a C program that takes a single integer (a `src` node ID) as a command-line argument and prints its *true* outgoing degree (the exact number of valid `dst` connections in the database).
3. The C program must query the SQLite database. To ensure accurate results for the corrupted nodes, your query must bypass the corrupted index and read from the main table data (e.g., using SQLite's `NOT INDEXED` clause or a full table scan).
4. Compile your C program to the executable path `/home/user/route_degree`.

Example execution expected by our automated systems:
`$ /home/user/route_degree 42`
`5`

Ensure your C program is robust, handles the SQLite connection properly, and prints ONLY the integer degree to stdout. Use the `sqlite3` C library (`-lsqlite3`).