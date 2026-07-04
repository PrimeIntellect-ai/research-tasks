You are a Database Reliability Engineer (DBRE) tasked with restoring a critical backup replication pipeline. Our configuration management system crashed, and the only surviving record of our multi-datacenter replication topology is a dashboard screenshot saved at `/app/topology.png`. 

Your goal is to write a Bash script at `/home/user/find_backup_route.sh` that determines the optimal (lowest latency) replication path from the `DB_PRIMARY` node to the `DB_ARCHIVE` node, subject to node storage constraints.

Here are the requirements:
1. **Extract the Topology:** Use OCR or vision tools (e.g., `tesseract` is available in the environment) to extract the graph edges and latencies from `/app/topology.png`. The image contains text lines representing edges, formatted like `SOURCE -> DESTINATION : LATENCY_MS`.
2. **Filter Capable Nodes:** We can only route backups through nodes that have at least 500GB of free disk space. A local SQLite database at `/app/nodes.db` contains a table `node_stats` with columns `node_name` (TEXT) and `free_space_gb` (INTEGER). Query this database to identify which nodes are eligible. `DB_PRIMARY` and `DB_ARCHIVE` are always eligible.
3. **Compute the Shortest Path:** Your Bash script must dynamically calculate the shortest valid path (lowest total latency) from `DB_PRIMARY` to `DB_ARCHIVE`, completely avoiding any intermediate nodes that have less than 500GB of free space.
4. **Output Format:** The script should output the results to `/home/user/best_route.txt`.
   - The first line must be the comma-separated sequence of nodes in the optimal path (e.g., `DB_PRIMARY,DB_X,DB_Y,DB_ARCHIVE`).
   - The second line must be the total integer latency of that path (e.g., `45`).

Your script should be robust and executable. Do not hardcode the extracted values in the final output file; the script must perform the extraction, querying, chaining, and graph traversal programmatically when run. Run your script to produce `/home/user/best_route.txt`.