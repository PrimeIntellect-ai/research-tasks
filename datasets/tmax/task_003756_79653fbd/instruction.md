You are a database administrator optimizing a notoriously slow NoSQL graph aggregation pipeline. The current pipeline calculates the shortest traversal paths across a logistics network and aggregates node-level delay metrics, but it is timing out in the database. 

To solve this, you have exported the NoSQL collections to JSON files and need to write a high-performance Rust program to process the graph offline.

Your task is to create a Rust utility that reads the exported graph data, computes the shortest paths for a set of queries, aggregates the node delays along those paths, and exports the results to a CSV file.

### Environment & Input Files
The data files are located in `/home/user/data/`:
1. `/home/user/data/nodes.json`: An array of JSON objects representing network nodes.
   Format: `[{"id": "A", "delay": 2}, {"id": "B", "delay": 5}]`
2. `/home/user/data/edges.json`: An array of JSON objects representing directed edges.
   Format: `[{"source": "A", "target": "B", "cost": 10}]`
3. `/home/user/data/queries.json`: An array of queries to execute.
   Format: `[{"query_id": "q1", "start": "A", "end": "E"}]`

### Requirements
1. Initialize a new Rust project named `graph_optimizer` in `/home/user/graph_optimizer`.
2. Write a Rust program that reads the three JSON files. You may use standard crates like `serde`, `serde_json`, and `csv`.
3. For each query, calculate the shortest path from the `start` node to the `end` node based on edge `cost`. (Use Dijkstra's algorithm).
4. Aggregate the total cost of the edges on the shortest path.
5. Aggregate the total `delay` of all nodes visited on the shortest path (including both the start and end nodes).
6. Export the aggregated results to `/home/user/results/optimized_paths.csv`.

### Output Format
The output CSV must strictly follow this structure (including the header row):
```csv
query_id,path,total_cost,total_delay
q1,A->C->B->D->E,12,11
```
*   `query_id`: The ID from the queries file.
*   `path`: The sequence of node IDs joined by `->`.
*   `total_cost`: The sum of edge costs along the path.
*   `total_delay`: The sum of node delays along the path.

### Execution
Compile your Rust program in release mode and run it to produce the output file. Ensure that the final file exists at `/home/user/results/optimized_paths.csv`.