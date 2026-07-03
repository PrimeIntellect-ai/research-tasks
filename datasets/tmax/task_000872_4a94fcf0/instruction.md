You are a Database Reliability Engineer (DBRE) responsible for verifying graph database backups. Your company's primary graph database failed, but fortunately, the daily backup was successfully exported into a relational SQLite database located at `/home/user/graph_backup.db`. 

However, you only need to restore a critical sub-graph for an incident investigation. You must extract a specific subset of the data using window functions to rank the nodes, and then map this relational data into a Cypher script that can be used to restore the graph.

The SQLite database `/home/user/graph_backup.db` has two tables:
1. `nodes` (id INTEGER PRIMARY KEY, hostname TEXT, region TEXT)
2. `edges` (source_id INTEGER, target_id INTEGER, latency REAL)

Your task is to write a script (in Python, Bash, or SQL) that performs the following:
1. **Analytical Aggregation & Windowing**: Identify the "Core Servers". A core server is defined as one of the top 2 servers in each `region` based on the *number of outgoing connections* (edges where the server is the `source_id`). If there is a tie in the count of outgoing connections, prioritize the server with the lowest `id`.
2. For each Core Server, calculate its `avg_out_latency` (the average latency of all its outgoing connections, rounded to 1 decimal place). If a server has no outgoing connections, its average latency should be `0.0`.
3. **Cross-representation Mapping**: Generate a Cypher file at `/home/user/restore.cypher` that rebuilds this subset of the graph.
   - First, create the nodes for the Core Servers using this exact format, ordered by id ascending:
     `CREATE (:Server {id: [ID], hostname: '[HOSTNAME]', region: '[REGION]', avg_out_latency: [LATENCY]});`
   - Second, create the relationships (edges) *only* if both the `source_id` and `target_id` are Core Servers. Order the edge creation statements by `source_id` ascending, then `target_id` ascending. Use this exact format:
     `MATCH (s:Server {id: [SOURCE_ID]}), (t:Server {id: [TARGET_ID]}) CREATE (s)-[:CONNECTS_TO {latency: [LATENCY]}]->(t);`

Place the node creation statements first, followed by an empty line, followed by the edge creation statements. 

Ensure the final file `/home/user/restore.cypher` is perfectly formatted as described above. You may use standard Linux utilities, SQLite3, and Python 3 to complete this task.