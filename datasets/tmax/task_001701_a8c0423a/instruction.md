You are a Database Reliability Engineer (DBRE) responsible for the global backup infrastructure. Our backup system routes large snapshots between data centers (DCs) using an internal network. The network topology and historical transfer logs are stored in a SQLite database at `/home/user/backups.db`.

Your task is to write a Go program at `/home/user/backup_router.go` that calculates the optimal routing path for a new backup transfer and analyzes recent performance along that path.

The SQLite database contains three tables:
1. `datacenters`:
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
2. `network_links`:
   - `source_id` (INTEGER)
   - `dest_id` (INTEGER)
   - `latency_ms` (INTEGER)
3. `transfer_logs`:
   - `id` (INTEGER PRIMARY KEY)
   - `source_id` (INTEGER)
   - `dest_id` (INTEGER)
   - `bytes_transferred` (INTEGER)
   - `duration_ms` (INTEGER)
   - `timestamp` (DATETIME)
   - `status` (TEXT) - e.g., 'SUCCESS', 'FAILED'

Your Go program must perform the following:
1. Read the network topology from the `network_links` and `datacenters` tables.
2. Implement a graph traversal algorithm to find the shortest path (lowest total `latency_ms`) from the datacenter named `DC-Alpha` to the datacenter named `DC-Omega`.
3. For *each hop* (link) in this shortest path, query the `transfer_logs` table. Use SQL analytical/window functions to calculate the average transfer speed (defined as `bytes_transferred / duration_ms`) of the **last 3 successful transfers** (ordered by `timestamp` descending) for that specific link. Note: Exclude failed transfers. If a link has fewer than 3 successful transfers, calculate the average over the available ones.
4. Output the routing plan to `/home/user/routing_plan.json`. The output must be a JSON array of objects representing the hops in order, with the exact keys: `source` (string, datacenter name), `dest` (string, datacenter name), and `avg_speed_bytes_per_ms` (float64, rounded to 2 decimal places).

Requirements:
- Ensure your Go module is initialized in `/home/user/` and you fetch necessary SQLite drivers (e.g., `github.com/mattn/go-sqlite3`).
- Do not modify the SQLite database.
- Execute your program so that the final `routing_plan.json` is generated.