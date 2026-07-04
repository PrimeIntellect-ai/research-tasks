You are a database administrator tasked with optimizing a slow permission-checking query. The existing NoSQL graph database is taking too long to compute access control paths. To analyze and optimize this, a snapshot of the permission graph has been exported as a JSON document to `/home/user/graph_data.json`.

The JSON file contains a dictionary with two keys:
- `nodes`: A list of node IDs (strings representing users, roles, and resources).
- `edges`: A list of dictionaries, each containing `source`, `target`, and `type` (representing directed relationships like `has_role`, `inherits`, `can_read`).

Your task is to write a highly optimized Python script at `/home/user/optimize_access.py` that processes this JSON file in-memory. The script must:
1. Load the graph from `/home/user/graph_data.json`.
2. Perform a graph traversal to find the shortest directed path (minimum number of edges) from the user node `"U_105"` to the resource node `"R_992"`.
3. Export the resulting shortest path to `/home/user/access_path.json` exactly in the following format:
   ```json
   {
       "path": ["U_105", "...", "R_992"],
       "distance": X
   }
   ```
   *(Where `X` is the integer number of edges in the path).*

If there are multiple shortest paths, any valid shortest path is acceptable. Make sure your Python script executes successfully and creates the requested JSON output file.