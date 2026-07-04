You are a Database Reliability Engineer managing the backup topology for a massive, multi-region database cluster.

We rely on a legacy compiled tool located at `/app/legacy_pathfinder` to generate the backup replication routes between our database nodes. You can run it by passing a cluster ID (e.g., `/app/legacy_pathfinder 42`). It outputs a CSV stream with columns: `source_node_id,target_node_id`.

Recently, we discovered that this legacy tool has a bug resembling an implicit cross-join: it outputs every possible connection between nodes, completely ignoring regional boundaries! 

We have an auxiliary SQLite database at `/home/user/backup_meta.db` containing a `nodes` table with the schema:
`CREATE TABLE nodes (node_id INTEGER PRIMARY KEY, region TEXT, is_global INTEGER);`

Your task is to write a Python script `/home/user/analyze_backups.py` that does the following:
1. Executes the legacy pathfinder for cluster ID `99`.
2. Filters the output to fix the "cross-join" bug. An edge from `source` to `target` is ONLY valid if:
   - Both nodes exist in the `backup_meta.db` database, AND
   - (`source.region` == `target.region` OR `source.is_global` == 1).
3. Builds a directed graph using the filtered valid edges.
4. Computes the PageRank of every node in this graph (using standard NetworkX PageRank with alpha=0.85).
5. Sorts the results by PageRank in descending order.
6. Paginates/filters the result to exactly the top 50 nodes.
7. Validates and saves the output to `/home/user/top_nodes.json` strictly matching this JSON schema:
   `[{"node_id": <int>, "pagerank": <float>}, ...]`

Ensure all dependencies (like `networkx`) are installed via pip if you need them. Save your final output file exactly as specified so our automated systems can grade the PageRank calculations.