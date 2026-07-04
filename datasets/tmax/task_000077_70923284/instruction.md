You are a Database Reliability Engineer managing cross-region database backups. Your storage network consists of several datacenters with varying network latencies and connection states (some links may be down for maintenance). 

An SQLite database is located at `/home/user/backup_network.db` containing the current topology and pending backup jobs. 

The database has the following schema:
- `datacenters` (id INTEGER PRIMARY KEY, name TEXT)
- `network_links` (source_id INTEGER, dest_id INTEGER, latency_ms INTEGER, status TEXT) 
  - Note: `status` can be 'UP' or 'DOWN'. Links are directed (one-way).
- `pending_backups` (backup_id TEXT PRIMARY KEY, source_dc_id INTEGER, dest_dc_id INTEGER, data_size_tb REAL)

Your task:
Write a Python script at `/home/user/plan_route.py` that takes a `backup_id` as a command-line argument. The script must:
1. Connect to the SQLite database.
2. Use parameterized queries to securely fetch the details for the given `backup_id`.
3. Retrieve the active ('UP') network topology.
4. Calculate the shortest path (lowest total latency) from the backup's source datacenter to its destination datacenter using a graph traversal algorithm (e.g., Dijkstra's).
5. Export the resulting routing plan to a JSON file named `/home/user/route_<backup_id>.json`.

The output JSON file must strictly match this structure:
```json
{
  "backup_id": "BKP-1234",
  "total_latency_ms": 45,
  "path": ["DC-Alpha", "DC-Beta", "DC-Gamma"]
}
```
Where `path` is an ordered list of datacenter names from source to destination.

After writing the script, execute it for the backup job with ID `BKP-9001`.