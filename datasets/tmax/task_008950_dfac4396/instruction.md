You are a data engineer debugging an ETL pipeline that processes a network routing knowledge graph. 

You have two files to work with:
1. `/home/user/data/nodes.json`: A NoSQL-style document dump of node metadata.
2. `/home/user/data/graph.db`: An SQLite database containing the network's edges.

There are a few issues you need to resolve to complete your task:
- The `edges` table in `graph.db` uses a soft-deletion pattern. You must only consider edges where `is_deleted = 0`.
- The `nodes.json` file contains various node types. You need to identify the exact node IDs for the node with `"role": "gateway"` and the node with `"role": "master_db"`.
- Use the active edges in the SQLite database to compute the shortest path (minimum number of hops) from the `gateway` node to the `master_db` node.

Write a Bash script (or series of shell commands) to extract the roles from the JSON, filter the SQLite graph edges, and calculate the minimum hops. 

Output ONLY the integer representing the minimum number of hops (edges) in the shortest path into the file `/home/user/shortest_path.txt`. 

For example, if the path is Gateway -> NodeA -> NodeB -> MasterDB, the output in the file should be exactly `3`.