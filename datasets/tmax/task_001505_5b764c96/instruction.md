You are a Database Reliability Engineer. We have an SQLite database containing our backup dependency graph at `/home/user/backups.db`. 

Recently, we discovered that the index on the `edges` table is corrupted, causing `WHERE` queries on the `source` column to return missing or stale rows. 

Your task is to write a Python script at `/home/user/analyze_backups.py` that bypasses the corrupted index, extracts the graph data, and performs graph analytics to help us plan our recovery. 

The database has the following schema:
- `nodes (id INTEGER PRIMARY KEY, name TEXT)`
- `edges (source TEXT, target TEXT, cost INTEGER)`

Your Python script must:
1. Connect to `/home/user/backups.db` using the standard `sqlite3` library.
2. Extract all rows from the `edges` table. To bypass the corrupted index, you must extract the entire table without using `WHERE source = ...` clauses (e.g., using a full table scan or the `NOT INDEXED` clause).
3. Compute the shortest path (minimum total cost) from the node named `'ROOT'` to the node named `'TARGET'`.
4. Calculate the in-degree (number of incoming edges) for all nodes in the graph to find the "most critical" backup node (the node with the highest in-degree). If there's a tie, pick the one that comes first alphabetically.
5. Validate and write your results to `/home/user/report.json` matching exactly this JSON schema:
```json
{
  "type": "object",
  "properties": {
    "shortest_path": {
      "type": "array",
      "items": {"type": "string"}
    },
    "total_cost": {"type": "integer"},
    "most_critical_node": {"type": "string"}
  },
  "required": ["shortest_path", "total_cost", "most_critical_node"]
}
```

Run your script to generate the `/home/user/report.json` file. Ensure that the script operates self-contained using only the Python standard library.