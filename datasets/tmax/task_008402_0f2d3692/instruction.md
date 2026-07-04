You are a Database Reliability Engineer managing a large multi-datacenter backup cluster. You have been tasked with identifying the lowest-latency replication path for backup validation between two critical datacenters: `DC-Alpha` (ID: 1) and `DC-Omega` (ID: 4).

A previous engineer started writing a C++ tool (`/home/user/backup_analyzer.cpp`) to calculate this, but they made a critical error. The SQL query embedded in the code contains an implicit cross join, causing it to return massive amounts of duplicated and incorrect edge data, and the shortest path algorithm itself was left unimplemented.

Your environment contains a SQLite database at `/home/user/backup_metadata.db` with three tables:
- `datacenters`: `id` (INTEGER), `name` (TEXT)
- `replication_links`: `source_id` (INTEGER), `target_id` (INTEGER), `latency_ms` (INTEGER)
- `backup_jobs`: `id` (INTEGER), `dc_id` (INTEGER), `status` (TEXT)

Your tasks:
1. Fix the SQL query in `/home/user/backup_analyzer.cpp`. The query must retrieve directed edges (`source_id`, `target_id`, `latency_ms`) from `replication_links`. However, you must ONLY include edges where the **target** datacenter currently has a backup job with a `status` of `'SUCCESS'`. Ensure you properly join `replication_links` and `backup_jobs` to avoid the cross-join cartesian product.
2. Implement the missing graph traversal function in the C++ file. Use Dijkstra's algorithm to find the shortest path (lowest total latency) from `DC-Alpha` (ID 1) to `DC-Omega` (ID 4) using the correctly filtered edges.
3. The C++ program must export the final calculated path and total latency to `/home/user/optimal_backup_path.json` in the exact following format:
   ```json
   {
     "path": [1, 2, 4],
     "total_latency_ms": 30
   }
   ```
4. Compile the C++ program using `g++ -O3 /home/user/backup_analyzer.cpp -lsqlite3 -o /home/user/backup_analyzer`.
5. Run the compiled executable to generate the JSON file.

You must rely entirely on C++ to perform the graph traversal and export the JSON. Do not write a separate Python or Bash script to bypass the C++ requirement.