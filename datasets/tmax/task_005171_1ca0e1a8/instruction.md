You are a Database Reliability Engineer (DBRE) responsible for the backup infrastructure. We have a distributed backup metadata database stored locally at `/home/user/backup_meta.db` (SQLite3 format). 

Recently, a script used to compute restoration plans broke. The SQL query used to calculate the total available backup size per node was returning massively inflated numbers due to an implicit cross join, and the script couldn't route between nodes efficiently.

Your task is to write a Go program at `/home/user/planner.go` that generates an optimal restore plan by combining correct database queries and graph traversal.

The SQLite database has three tables:
1. `nodes` 
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT UNIQUE)
2. `backups`
   - `id` (INTEGER PRIMARY KEY)
   - `node_id` (INTEGER)
   - `size_gb` (INTEGER)
   - `status` (TEXT) - can be 'COMPLETED' or 'FAILED'
3. `links`
   - `source_id` (INTEGER)
   - `target_id` (INTEGER)
   - `latency_ms` (INTEGER)

Requirements for `/home/user/planner.go`:
1. The program must accept exactly two command-line arguments: a source node name and a target node name (e.g., `go run planner.go Alpha Epsilon`).
2. **Graph Traversal:** The program must read the network topology from the `links` table and compute the shortest path (lowest total latency) from the source node to the target node. Note that links are directional.
3. **Complex Querying:** For every node in the computed shortest path (including source and target), the program must calculate the sum of `size_gb` for all backups with a 'COMPLETED' status. You must fix the implicit cross join issue by using proper explicit `JOIN`s and `GROUP BY` clauses. Use parameterized queries when filtering.
4. **Export:** The program must output the final plan to a JSON file located at `/home/user/restore_plan.json`.

The exported JSON must strictly follow this format:
```json
{
  "path": ["Alpha", "Beta", "Delta", "Epsilon"],
  "total_latency_ms": 45,
  "total_backup_gb": 1250
}
```
Where `total_backup_gb` is the sum of the completed backup sizes for all nodes included in the `path`.

Write the code, initialize the Go module in `/home/user`, install any needed SQLite drivers (like `github.com/mattn/go-sqlite3`), and run your program with the arguments `Alpha` and `Epsilon`. Ensure the output file is generated correctly.