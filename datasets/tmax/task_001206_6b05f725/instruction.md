You are a data analyst tasked with analyzing a large logistics dataset containing city nodes and route edges. We need to compute the PageRank of all distribution centers and find the shortest path costs from a central hub to all other locations. 

You have been provided with two CSV files:
1. `/home/user/data/nodes.csv` (columns: `node_id`, `node_type`, `name`)
2. `/home/user/data/edges.csv` (columns: `source`, `target`, `travel_time`)

To process this data efficiently, you must use our internal graph library located at `/app/fast_graph_analytics-1.2.0`. However, the previous maintainer left the package in a slightly broken state. It currently fails to build its performance-critical C extension, causing it to fall back to an extremely slow pure-Python mode or crash. 

Your tasks are:
1. Identify and fix the build configuration issue in `/app/fast_graph_analytics-1.2.0`.
2. Build and install the package into your Python environment.
3. Write a Python script at `/home/user/analyze_logistics.py` that:
   - Uses the `fast_graph_analytics` library to parse the relational CSV data into a directed graph representation.
   - Computes the shortest path travel time from the node with `node_id` = `"HUB_001"` to all other nodes.
   - Computes the PageRank scores for all nodes.
   - Exports the results to `/home/user/analysis_output.json`.

The output file `/home/user/analysis_output.json` must exactly follow this format:
```json
{
  "pagerank": {
    "NODE_ID": 0.0152,
    ...
  },
  "shortest_paths_from_HUB_001": {
    "NODE_ID": 145.2,
    ...
  }
}
```

Make sure your solution uses the high-performance C backend of the library, as the evaluator will be strictly checking the accuracy and precision of your graph computations against a golden reference, which relies on the C extension's floating-point precision logic.