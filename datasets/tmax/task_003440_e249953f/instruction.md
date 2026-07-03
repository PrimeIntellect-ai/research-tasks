You are a database administrator tasked with optimizing and querying a routing database. We have an SQLite database located at `/home/user/routing.db` that contains a network graph of routers and their connections. 

However, queries on this database have been extremely slow. It appears the previous administrator created a redundant or poorly designed index that is causing performance issues, and we need to compute shortest paths efficiently.

Your task is to write a Python script `/home/user/optimize_and_query.py` that does the following:
1. Connects to `/home/user/routing.db`.
2. Drops any existing indexes on the `edges` table and creates a single optimal composite index to speed up graph traversal from a source node to a target node. The index should optimize filtering by `source_id` and joining with `target_id`.
3. Executes a single SQL query using a `WITH RECURSIVE` Common Table Expression (CTE) to find the shortest paths from the node with name `'Router_START'` to the node with name `'Router_END'`.
4. The query must only traverse through nodes that have `status = 'active'` (the start and end nodes are also guaranteed to be active).
5. To avoid infinite loops, limit the path depth to a maximum of 7 edges.
6. The query should return the paths sorted by the `total_weight` of the path in ascending order.
7. Apply pagination to return exactly the top 3 paths (LIMIT 3).
8. The result for each path must be aggregated to provide:
   - `path_names`: A comma-separated string of router names in the path (e.g., "Router_START,Router_A,Router_END").
   - `total_weight`: The sum of the weights of the edges in the path.
   - `hop_count`: The number of edges in the path.
9. Your script must output the final results as a JSON array of objects to `/home/user/top_paths.json`. Each object should have the keys `path_names`, `total_weight`, and `hop_count`.

Database Schema:
- Table `nodes`:
  - `id` (INTEGER PRIMARY KEY)
  - `name` (TEXT)
  - `status` (TEXT) - can be 'active' or 'offline'
- Table `edges`:
  - `source_id` (INTEGER)
  - `target_id` (INTEGER)
  - `weight` (REAL)

Note: Do not modify the data in the tables, only the indexes. The output JSON file must strictly match the specified format.