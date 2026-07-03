You are a Database Reliability Engineer managing backups for a globally distributed database cluster. You need to automate the planning of a critical cluster restore operation. 

There are two main components to this task:

1. **Network Topology Recovery**:
You have been given a network topology diagram in an image file at `/app/network_latencies.png`. This diagram shows the backup storage nodes (e.g., NodeA, NodeB) and the transfer latencies (in milliseconds) between them in a simple text format. You need to extract this graph structure (nodes, edges, and weights). Tesseract OCR is installed on the system.

2. **Backup Metadata and Indexing**:
You have an SQLite database at `/home/user/backups.db` containing millions of rows of backup logs. 
Table schema: `CREATE TABLE backup_catalog (id INTEGER PRIMARY KEY, node TEXT, timestamp INTEGER, is_full INTEGER, size_bytes INTEGER);`
This table is currently unindexed. Querying for the latest full backup is extremely slow.

Your objective is to:
1. Optimize the SQLite database by designing and applying the correct index strategy so that querying for the most recent full backup (`is_full = 1`) takes less than 100 milliseconds.
2. Extract the graph data from `/app/network_latencies.png`.
3. Write a primary executable Bash script at `/home/user/plan_restore.sh` that takes a single argument, the `<target_node>` (e.g., `NodeF`).
4. The script must:
   - Query `/home/user/backups.db` to identify the `node` that contains the backup with the maximum `timestamp` where `is_full = 1`.
   - Calculate the shortest path (minimum total latency) from that source node to the `<target_node>` using the network graph extracted from the image.
   - Output *only* the total minimum latency (an integer) to standard output.

Constraints:
- You must write `/home/user/plan_restore.sh` using Bash as the primary orchestration language (you may use embedded `awk`, `jq`, or `python` within the script for graph traversal algorithms like Dijkstra's, provided it's invoked from the bash script).
- Your script must execute in less than 1.0 seconds. If you fail to index the database properly, the SQLite query alone will exceed this time limit.
- Do not hardcode the source node or the graph in your script; your script must parse the database and your OCR output dynamically.

Ensure `/home/user/plan_restore.sh` has executable permissions.