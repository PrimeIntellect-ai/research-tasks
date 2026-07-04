You are a database reliability engineer managing backups for a large graph database. The backup system exports graph data into an intermediate SQLite database before archiving. Recently, a corrupted index in the production database led to some "stale" edge records being exported—these are relationships where the target node was deleted, but the edge remained.

Your task is to analyze the intermediate SQLite backup, summarize the corruption, and generate a remediation script in Cypher to clean up the production graph database.

The SQLite database is located at `/home/user/graph_backup.db`. 
It contains two tables:
1. `nodes` with columns `node_id` (INTEGER)
2. `edges` with columns `edge_id` (INTEGER), `source_id` (INTEGER), `target_id` (INTEGER), and `rel_type` (TEXT)

A "stale edge" is defined as any row in `edges` where the `source_id` exists in the `nodes` table, but the `target_id` DOES NOT exist in the `nodes` table.

Please perform the following using Python:
1. Write a script `/home/user/analyze_graph.py` that connects to the SQLite database.
2. Identify all stale edges based on the condition above.
3. Calculate the count of these stale edges grouped by their `rel_type`. Write this summary to `/home/user/stale_summary.txt` in the format `rel_type: count`, sorted alphabetically by `rel_type`, with one entry per line.
4. Generate a Cypher script at `/home/user/cleanup.cypher` containing the exact commands to delete these specific stale relationships in production. For each stale edge, write a single line of Cypher using this exact format:
`MATCH (s)-[r:REL_TYPE]->() WHERE s.node_id = SOURCE_ID AND r.edge_backup_id = EDGE_ID DELETE r;`
Replace `REL_TYPE`, `SOURCE_ID`, and `EDGE_ID` with their respective values from the stale edges. Order the Cypher commands by `EDGE_ID` in ascending order.