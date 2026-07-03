You are a database administrator tasked with optimizing and analyzing query routing in a complex microservice and database replication topology.

We have an SQLite database located at `/home/user/db_topology.db` that contains the dependency graph of our infrastructure. The database has two tables:
1. `nodes` 
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `node_type` (TEXT)
2. `edges`
   - `source_id` (INTEGER, foreign key to nodes.id)
   - `target_id` (INTEGER, foreign key to nodes.id)
   - `latency_ms` (INTEGER)
   - `connection_type` (TEXT)

Your goal is to write a Python script at `/home/user/analyze_routing.py` that calculates the shortest path (by total `latency_ms`) from the node named `'API_Gateway'` to the node named `'User_Master'`. 

You can compute this using a recursive CTE in SQLite, complex joins, or by pulling the data into Python and performing a graph traversal—whichever is most efficient.

Requirements:
1. The script must query `/home/user/db_topology.db`.
2. The script must calculate the minimum latency path from `'API_Gateway'` to `'User_Master'`.
3. The script must format the output and save it to `/home/user/routing_result.json`.
4. The JSON output must strictly adhere to the following schema:
```json
{
  "source": "API_Gateway",
  "destination": "User_Master",
  "total_latency_ms": <integer>,
  "path_nodes": [
    "API_Gateway",
    "<Intermediate_Node_1>",
    "...",
    "User_Master"
  ]
}
```

Run your script to generate the JSON file once you are done.