You are a data analyst working with a dataset of transaction networks. You have been given two CSV files representing a directed graph:
1. `/home/user/nodes.csv` - Contains columns `id` (string) and `name` (string).
2. `/home/user/edges.csv` - Contains columns `source` (string), `target` (string), and `weight` (float).

Your task is to write a Rust application that processes this graph data, materializes a specific graph projection, and extracts insights using parameterized queries. 

Please perform the following steps:
1. Create a new Rust project named `graph_analyzer` in `/home/user/`.
2. The Rust program must read the CSV files and load them into a SQLite database file located at `/home/user/graph.db`. 
3. **Index Strategy Design:** Create appropriate indexes on the `edges` table to optimize for path traversal (specifically, looking up outgoing and incoming edges for any given node).
4. **Graph Projection & Materialization:** Using a single SQL statement (executed from your Rust code), create a new table named `two_hop_paths` that materializes all exactly 2-hop paths in the graph. The table must have columns `start_node`, `end_node`, and `total_weight`. The `total_weight` is the sum of the weights of the two edges forming the path.
5. **Parameterized Query Construction:** Write a function in your Rust application that takes a starting node `id` as a parameter. It must query the `two_hop_paths` table securely using a parameterized SQL query to find all 2-hop destinations from that node, ordered by `total_weight` descending.
6. **Output Schema Validation:** Execute this function for the starting node `"N001"`. Export the results to a JSON file at `/home/user/results.json`. The output must be an array of objects, strictly adhering to this schema:
   `[ { "destination": "string", "weight": float } ]`
   Only include the top 3 highest-weight paths.

Use `cargo run` to execute your program and ensure `/home/user/results.json` is generated correctly. You may use crates like `rusqlite`, `csv`, `serde`, and `serde_json`.

Note: Ensure the database connection is closed properly so the file is written to disk. The test suite will query `/home/user/graph.db` to verify the indexes and materialized table.