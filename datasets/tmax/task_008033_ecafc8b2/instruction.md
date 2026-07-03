You are a Data Engineer building an ETL pipeline. You need to process a dataset representing a data lineage graph, compute shortest paths, calculate analytical metrics using SQL window functions, and export the results to a JSON file.

Setup:
The graph data is provided in two CSV files (which already exist on your system):
1. `/home/user/nodes.csv` - Contains node information.
   Columns: `id` (string), `cost` (integer)
2. `/home/user/edges.csv` - Contains directed edges.
   Columns: `src` (string), `dst` (string), `weight` (integer)

Your task:
1. Initialize a Go module in `/home/user/etl_pipeline`.
2. Write a Go program (`main.go`) that parses the CSV files.
3. Compute the shortest path distance from the root node `"ROOT"` to all reachable nodes in the graph using Dijkstra's algorithm. (The distance to `"ROOT"` itself is 0).
4. Load the reachable nodes, their shortest path `distance`, and their `cost` into a SQLite database (you may use an in-memory database or a file via `github.com/mattn/go-sqlite3`).
5. Execute a SQL query on this data that retrieves the following fields for each reachable node:
   - `id`
   - `distance`
   - `cost`
   - `cumulative_cost`: The running total of `cost` ordered by `distance` ascending, and then by `id` ascending. (e.g., using `SUM() OVER (...)`)
   - `cost_rank`: The rank of the node's `cost` (descending) compared to other nodes at the exact same `distance`. (e.g., using `RANK() OVER (...)`)
6. Export the results of this query as a JSON array of objects to exactly `/home/user/summary.json`. Sort the JSON array by `distance` ascending, then `id` ascending.

The final output in `/home/user/summary.json` must look exactly like this format:
```json
[
  {
    "id": "ROOT",
    "distance": 0,
    "cost": 10,
    "cumulative_cost": 10,
    "cost_rank": 1
  },
  ...
]
```

Requirements:
- Ensure all Go code compiles and runs successfully.
- You must use Go and SQLite queries to perform the aggregations.
- Nodes not reachable from `"ROOT"` should be excluded from the final JSON.