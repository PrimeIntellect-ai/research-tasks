You are a data engineer managing an ETL pipeline for a supply chain logistics network. 

We have an SQLite database located at `/home/user/supply_chain.db`. Recently, a database migration caused the materialized view system to fail. As a result, the `cached_shortest_paths` table contains corrupted, stale data and should NOT be used under any circumstances.

Your task is to dynamically compute the optimal (fastest) active route from the facility named `Origin-Alpha` to `Dest-Omega` by reading directly from the base relational tables, mapping the data into a graph, performing a shortest-path traversal, and exporting the results.

The base tables are:
1. `facilities`: Contains `id` (INTEGER) and `name` (TEXT).
2. `connections`: Contains `rowid` (implicit SQLite ID), `source_id` (INTEGER), `dest_id` (INTEGER), `transit_time` (INTEGER), and `cost` (INTEGER).
3. `disruptions`: Contains `connection_id` (INTEGER, refers to `connections.rowid`) and `status` (TEXT). If a connection has a record here with `status = 'active'`, that connection is currently blocked and cannot be traversed.

Your objective:
1. Write a script (in the language of your choice) to query the active graph (excluding any connections that have an 'active' disruption).
2. Compute the shortest path from `Origin-Alpha` to `Dest-Omega` minimizing `transit_time`.
3. Export the query and traversal results to a JSON document at `/home/user/optimal_route.json`.

The JSON file must have exactly this structure:
```json
{
  "total_transit_time": <integer>,
  "total_cost": <integer>,
  "path": ["Origin-Alpha", "Intermediate-Node-1", ..., "Dest-Omega"]
}
```

Constraints:
- You may install any packages you need (e.g., Python's `networkx`, `pandas`, etc.) via standard package managers.
- Do NOT use the `cached_shortest_paths` table.
- Use `transit_time` as the primary weight for the shortest path. `cost` should just be summed along the chosen path.