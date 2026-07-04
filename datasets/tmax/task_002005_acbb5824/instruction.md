You are a database administrator. We have an SQLite database at `/home/user/graph.db` that represents a knowledge graph of system components. 

Recently, the database experienced a crash, and queries using the index `idx_edges_target` are returning stale, incorrect rows. 

Your task is to:
1. Repair the corrupted index in the SQLite database `/home/user/graph.db`.
2. Write a Rust program at `/home/user/graph_analyzer/src/main.rs` (create the Cargo project appropriately in `/home/user/graph_analyzer`) that connects to this database using the `rusqlite` crate.
3. The Rust program must execute a parameterized graph analytics query that:
   - Calculates the total incoming edge weight for each target node.
   - Uses a window function to assign a rank to each node based on its total incoming weight, partitioned by the node's `type` (Rank 1 is the highest weight).
   - Filters out any nodes whose total incoming weight is strictly less than a parameterized threshold value provided as the first command-line argument to the Rust program.
   - Returns only the nodes with Rank 1 for each type.
4. Run your Rust program with a threshold argument of `15.0`.
5. Write the final results to `/home/user/top_nodes.csv` in the exact format: `type,name,total_weight` (with a header row, sorted alphabetically by `type`).

Database Schema for reference:
- `nodes(id INTEGER PRIMARY KEY, type TEXT, name TEXT)`
- `edges(source INTEGER, target INTEGER, weight REAL)`

Ensure you run your Rust program so the CSV file is generated. Do not leave the task until `/home/user/top_nodes.csv` is fully populated.