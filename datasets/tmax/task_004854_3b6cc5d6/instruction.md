You are a data analyst working on a logistics network. You have been provided with network data in CSV format and need to write a C++ program to analyze it, computing optimal routing paths and aggregating cost metrics.

You have three files located in `/home/user/`:
1. `nodes.csv` - Contains `node_id,processing_delay`. The `processing_delay` is an integer representing the cost to route through this node.
2. `edges.csv` - Contains `source,target,transit_cost`. The `transit_cost` is an integer representing the cost to travel between two nodes. All edges are directed.
3. `queries.csv` - Contains `query_id,start_node,end_node`.

Write a C++ program named `/home/user/analyze_network.cpp` that parses these CSV files and computes the optimal (lowest total cost) path for each query. 

The "total cost" of a path is defined as:
`Sum of transit_costs of all edges in the path` + `Sum of processing_delays of all INTERMEDIATE nodes in the path`.
(Do not include the processing delay of the `start_node` or `end_node`).

If multiple paths have the same lowest total cost, choose the one with the fewest number of edges. If there is still a tie, choose the path that comes first lexicographically (e.g., A-B-C over A-D-C).

Your program must output the results as a strictly formatted JSON array to `/home/user/results.json`. You may install and use `nlohmann-json3-dev` (via `sudo apt-get update && sudo apt-get install -y nlohmann-json3-dev` if needed, though you can also format the JSON manually).

The output `results.json` must exactly match this schema:
```json
[
  {
    "query_id": "q1",
    "path": ["A", "B", "C"],
    "total_transit_cost": 10,
    "total_delay_cost": 5,
    "total_cost": 15
  }
]
```

Compile your code using `g++ -O3 -std=c++17 /home/user/analyze_network.cpp -o /home/user/analyze_network` and run it to produce the `results.json` file.