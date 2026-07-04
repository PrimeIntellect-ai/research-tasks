You are a database administrator acting as a performance engineer. We have exported data from our NoSQL network routing database into two JSON files: `/home/user/nodes.json` and `/home/user/edges.json`. 

The `nodes.json` file contains a list of server nodes, each with a string `id` and an integer `load`.
The `edges.json` file contains a list of directed network links, each with a `src` (source node id), `dst` (destination node id), and an integer `latency`.

Your task is to write a C++ program at `/home/user/analyze_routing.cpp` that performs the following operations:
1. Analyzes the schemas of both JSON files and loads the data into an in-memory graph.
2. Computes the shortest path (based on `latency`) from the node with id `"Gateway"` to the node with id `"Database"`.
3. Performs a cross-entity aggregation by summing the `load` of all nodes present on this shortest path (including the Gateway and Database nodes).
4. Exports the resulting optimized route and aggregated metrics to a JSON file at `/home/user/result.json` in the exact following format:
```json
{
  "path": ["Gateway", "NodeX", "Database"],
  "total_latency": 15,
  "total_load": 45
}
```

**Environment constraints & hints:**
- You must use C++ to solve this task.
- To make JSON parsing easier, the `nlohmann/json` header is already provided for you at `/home/user/json.hpp`. You can include it via `#include "json.hpp"`.
- You can compile your code using `g++ -O3 -std=c++17 /home/user/analyze_routing.cpp -o /home/user/analyze_routing`.
- Run your compiled program to generate `/home/user/result.json`.

Please write the C++ code, compile it, run it, and ensure `/home/user/result.json` is correctly generated.