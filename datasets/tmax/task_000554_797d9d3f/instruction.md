You are a data analyst tasked with processing network infrastructure data. We have exported the network topology into two CSV files located in `/home/user/data/`:

1. `/home/user/data/nodes.csv` (columns: `id`, `name`, `type`)
2. `/home/user/data/edges.csv` (columns: `src`, `dst`, `cost`)

You need to write a Rust program (initialize it in `/home/user/graph_analyzer`) that acts as an in-memory graph query engine. The program must:
1. Parse the CSV files and materialize the graph in memory. The edges are directed.
2. Perform a parameterized shortest-path computation (using Dijkstra's or a similar algorithm) from a given starting node.
3. Filter the reachable nodes by dropping any node that has a specific `type`, and only keeping nodes where the total shortest path cost from the start node is less than or equal to a given `max_cost`. The start node itself should be excluded from the final results.
4. Sort the remaining nodes strictly alphabetically by their `name` in descending order.
5. Paginate the results based on a `page_size` and a 1-indexed `page_number`.
6. Output the requested page of results to a JSON file.

You must run your program to answer the following specific query and write the output to `/home/user/output.json`:
- **Start Node**: `N1`
- **Max Cost**: `35`
- **Exclude Type**: `Maintenance`
- **Page Size**: `2`
- **Page Number**: `2` (1-indexed, meaning the second page of results)

The expected format of `/home/user/output.json` is a JSON array of objects, containing only the nodes on the requested page, with their computed shortest path costs. Do not pretty-print; output it as a single-line JSON array. Example:
`[{"id":"N9","name":"StationZ","cost":15},{"id":"N5","name":"StationY","cost":20}]`

Use any standard Rust crates you need (e.g., `csv`, `serde`, `serde_json`, `petgraph`, etc.). You are responsible for configuring the Cargo project and running it to produce the correct output file.