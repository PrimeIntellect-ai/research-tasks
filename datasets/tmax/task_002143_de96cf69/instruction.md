You are a data analyst investigating a logistics network. You have been given two CSV files representing a graph of transit hubs and the routes between them. 

You need to write a Python script `/home/user/process_graph.py` that calculates the optimal (shortest/least cost) path between a specific starting hub and a destination hub.

The data files are:
1. `/home/user/nodes.csv` 
   Columns: `node_id`, `node_type`, `base_value`
2. `/home/user/edges.csv`
   Columns: `src`, `dst`, `cost`
   *(Note: Edges are directed. A row where src=A and dst=B means you can travel from A to B at the given cost).*

Your objective:
Write a Python script (using only standard libraries) that reads these files and computes the shortest path from `node_id` **"A"** to `node_id` **"E"** based on the edge `cost`. 

Once you find the shortest path, you must also calculate the sum of the `base_value` of all nodes along that exact path (including both the starting node "A" and the destination node "E").

Your script should execute and output a JSON file to `/home/user/result.json` with the following exact schema:
```json
{
  "shortest_path_cost": <integer_total_cost_of_path>,
  "total_node_value": <integer_sum_of_base_values_on_path>,
  "path": ["<node_id_1>", "<node_id_2>", "..."]
}
```

Constraints:
- You must use standard Python 3 libraries (e.g., `csv`, `json`, `heapq`). No external packages like `networkx` or `pandas` are installed.
- Ensure the sum of `base_value` correctly casts the CSV strings to integers.