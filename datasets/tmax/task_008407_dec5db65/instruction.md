You are a database administrator tasked with optimizing and analyzing an undocumented SQLite database located at `/home/user/system_graph.db`. This database contains a directed graph structure, but the schema is not documented.

Your tasks are to:

1. **Reverse Engineer the Data Model**: Inspect the database to find the table that represents directed edges. This table contains exactly two integer columns (representing the source and destination node IDs). Write the original `CREATE TABLE` statement for this exact table to a file named `/home/user/schema.txt`.

2. **Design an Index Strategy**: The database is currently experiencing slow query performance when looking up adjacent nodes. Create appropriate indexes on the edge table to optimize queries that filter by the source node, and queries that filter by the destination node. Name the indexes `idx_source` and `idx_dest` respectively.

3. **Parameterized Graph Analytics**: Write a Python script `/home/user/graph_metrics.py` that calculates the total degree centrality (in-degree + out-degree) of a specific node. 
   - The script must accept a single integer node ID as a command-line argument.
   - It must query the database using **parameterized queries** (e.g., using `?` placeholders) to prevent SQL injection and improve query plan caching.
   - It should print only the total integer degree to standard output.

4. **Execution**: Run your script for node ID `42` and save the output to `/home/user/node_42_metrics.txt`.

Ensure all requested files (`schema.txt`, `graph_metrics.py`, `node_42_metrics.txt`) are created in `/home/user/` and that the database `/home/user/system_graph.db` has been modified to include the new indexes.