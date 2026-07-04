You are a data engineer responsible for fixing and maintaining an ETL pipeline that processes network topology graphs. 

We have an SQLite database located at `/home/user/topology.db`. This database contains two tables representing a directed property graph:
1. `nodes` - Contains node information.
   - `id` (INTEGER PRIMARY KEY)
   - `role` (TEXT) - e.g., 'compute', 'storage', 'router'
2. `edges` - Contains directed edge information.
   - `src` (INTEGER) - Foreign key to nodes.id
   - `dst` (INTEGER) - Foreign key to nodes.id
   - `latency` (INTEGER) - The cost/weight of the edge

**Incident Report:**
The database recently experienced an unexpected crash, and we suspect the index `idx_edges_src` on the `edges` table is corrupted and returning stale/phantom rows during query execution. 

**Your Objective:**
1. **Database Repair:** First, execute a repair on the database by dropping the `idx_edges_src` index and recreating it on the `src` column of the `edges` table. Alternatively, you can run the `REINDEX` command to fix all indexes.
2. **Graph Projection:** We need to project a specific subgraph. Filter the graph to ONLY include nodes where `role = 'compute'`. You must ignore any edges that connect to or from a non-compute node.
3. **Relationship Mapping & Aggregation:** In this compute-only subgraph, find all directed "triangles". A directed triangle is a cycle of exactly 3 edges connecting 3 distinct nodes (e.g., A -> B -> C -> A). 
4. **Summarization:** Calculate the total latency for each valid triangle (the sum of the `latency` of its 3 edges). Find the triangle with the **minimum** total latency.
5. **Output:** Write the single minimum total latency value (an integer) to `/home/user/min_latency.txt`. Do not include any other text or characters in the file.

Write the necessary SQL queries or scripts to accomplish this task. You may use standard CLI tools, Bash, Python, or standard SQLite commands.