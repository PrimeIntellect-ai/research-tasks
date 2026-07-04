You are a Database Reliability Engineer (DBRE) investigating a backup system failure. Our backup dependency topology is stored as a graph in an SQLite database at `/home/user/backup_topology.db`. 

Recently, the database experienced a partial corruption. Specifically, the index `idx_edges_source` on the `edges` table is corrupted and returning stale or missing rows, causing standard backup traversal queries to fail or miss targets.

Your task is to:
1. Fix or bypass the corrupted index in the SQLite database so that queries return the correct, up-to-date rows.
2. Write a script (in Python or Bash) to traverse the backup graph. You need to identify all downstream backup destination nodes that are reachable starting from the node with the `hostname` equal to `main-db-server`. 
3. The database schema has two tables:
   - `nodes`: `id` (INTEGER PRIMARY KEY), `hostname` (TEXT)
   - `edges`: `source_id` (INTEGER), `target_id` (INTEGER)
4. Materialize the result of your graph traversal. Export the hostnames of all reachable nodes (excluding `main-db-server` itself) as a JSON array of strings, sorted alphabetically, to `/home/user/downstream_targets.json`.

Ensure your query plan uses a recursive CTE or an application-side graph traversal (like NetworkX) on the corrected data.