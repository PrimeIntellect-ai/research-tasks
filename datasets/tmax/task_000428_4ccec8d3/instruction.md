You are a data analyst acting as a data engineer. We have a set of CSV files representing a financial transaction network, but the system that exported them had a "corrupted index" issue: it exported historical, stale rows instead of just the current state of relationships.

Your task is to build a Rust pipeline that ingests these CSVs, cleans the stale data, constructs an in-memory graph, and executes a specific pathing query, outputting the result to a JSON file.

Setup:
You have two files located in `/home/user/data/`:
1. `/home/user/data/nodes.csv` (Columns: `id`, `type`)
2. `/home/user/data/edges.csv` (Columns: `source`, `target`, `timestamp`, `weight`)

Requirements:
1. Create a new Rust project in `/home/user/graph_pipeline`.
2. Write a Rust program that reads the CSV files.
3. Clean the edge data (handling the stale rows):
   - There may be multiple rows for the same `(source, target)` pair. 
   - You must group the edges by `(source, target)` and keep ONLY the edge with the strictly highest `timestamp`.
   - After finding the most recent edge for a pair, check its `weight`. If the `weight` is strictly less than 0, it means the connection was "deleted" and must NOT be added to your graph.
4. Construct a directed graph from the cleaned edges.
5. Execute a graph query to find all unique nodes reachable from the node with id `"N001"` within exactly 1 or 2 hops. (Do not include `"N001"` itself in the output unless a cycle leads back to it).
6. Validate and format the output: Output a JSON file at `/home/user/output.json` with the following strict schema:
   `{"reachable_nodes": ["<id1>", "<id2>", ...]}`
   The array of IDs MUST be sorted alphabetically.

Constraints:
- Use Rust. You may use standard crates like `csv`, `serde`, `serde_json`, and `petgraph` by defining them in your `Cargo.toml`.
- Compile and run your code to produce `/home/user/output.json`.