You are assisting a compliance officer auditing a complex corporate network for money laundering risks. Specifically, you are looking for hidden circular ownership structures (where a company ultimately owns a stake in itself through subsidiaries), which is a major compliance red flag.

You have been provided with a SQLite database at `/home/user/corporate_audit.db`. 
The database contains a single table:
`ownership_graph (owner_id INTEGER, subsidiary_id INTEGER)`

Your tasks are to:
1. Write a Python script at `/home/user/detect_cycle.py` that connects to this database and executes a single Recursive Common Table Expression (CTE) query to find the shortest circular ownership path starting from company ID `1001` and returning to `1001`.
2. The script must write the path of the cycle as a comma-separated list of IDs to `/home/user/cycle.txt`. For example, if 1001 owns 200, 200 owns 300, and 300 owns 1001, the output in the file should be exactly: `1001,200,300,1001`
3. The table currently has no indexes, making recursive graph traversals highly inefficient for large datasets. Determine the most critical index needed to optimize your recursive CTE (which repeatedly looks up the subsidiaries of a given owner). 
4. Execute the SQL command to create this index in the database. Name the index `idx_owner_sub`.
5. After creating the index, dump the `sql` text of this newly created index from the `sqlite_master` table into `/home/user/index_schema.txt`.

Ensure your Python script relies on SQL's recursive capabilities to perform the graph traversal, rather than fetching all rows and computing the path in Python memory.