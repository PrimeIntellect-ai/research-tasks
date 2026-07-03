You are a data engineer building an ETL pipeline. You have been given a SQLite database containing a dependency graph at `/home/user/graph.db`. 

The database has two tables:
1. `nodes`: `id` (INTEGER PRIMARY KEY), `name` (TEXT), `category` (TEXT)
2. `edges`: `source_id` (INTEGER), `target_id` (INTEGER), `weight` (REAL)

Your task is to write a Python script at `/home/user/etl_graph.py` that does the following:

1. **Optimize**: Execute a SQL command within your script to create an index on the `edges` table that optimizes retrieving outgoing edges for a given `source_id`. Name the index `idx_edges_source`.
2. **Query (Graph Traversal)**: Write a single SQL query using a Recursive CTE to traverse the graph starting from the node with `id = 42`. You need to find all edges in the subgraph reachable from node `42` up to a maximum depth of 3. 
   - Depth 1 = direct outgoing edges from node 42.
   - Depth 2 = outgoing edges from the targets of Depth 1.
   - Depth 3 = outgoing edges from the targets of Depth 2.
3. **Join**: In the same query, join the traversal results with the `nodes` table to retrieve the `name` and `category` of every `target_id` found in the traversal.
4. **Export**: Export the final query results to a JSON file at `/home/user/subgraph.json`. The JSON must be an array of objects with the exact following keys:
   - `source_id` (integer)
   - `target_id` (integer)
   - `target_name` (string)
   - `target_category` (string)
   - `depth` (integer)
   
   Sort the JSON array by `depth` ascending, and then by `target_id` ascending.

Run your script to produce the `/home/user/subgraph.json` file.