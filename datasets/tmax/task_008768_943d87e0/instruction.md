You are assisting a researcher who is organizing biological network datasets. 

The researcher has an SQLite database located at `/home/user/research_data.db`. The database contains a graph structure representing interactions between different biological entities. Unfortunately, the database crashed during a previous bulk update, and it is known that the index `idx_rel_src` on the relations table is corrupted. If SQLite's query optimizer decides to use this index, it returns stale "ghost" rows that invalidate the analysis.

Your objective is to write a Python script at `/home/user/analyze.py` that performs the following tasks:
1. Reverse engineers the data model of `/home/user/research_data.db` to identify the tables containing the nodes (entities and their types) and the directed edges (relations with weights and timestamps).
2. Extracts the "active" graph. Because the data represents a timeseries of observations, there may be multiple edge records for the same `(source, destination)` pair. The active graph consists ONLY of the edge with the highest `timestamp` for each `(source, destination)` pair. 
3. **CRITICAL:** You must write your SQL query in a way that explicitly forces SQLite to *bypass* the corrupted `idx_rel_src` index (for example, by using the `NOT INDEXED` clause). You should analyze the query plan to ensure the index is not used.
4. Using the active graph, calculate the average outgoing edge weight for each entity *type*. To do this, sum the weights of all active outgoing edges from nodes of a specific type, and divide by the number of active outgoing edges originating from that type.
5. Identify the entity type with the highest average outgoing edge weight.
6. Write the exact string of that entity type to `/home/user/top_type.txt`.

Constraints:
- Use only Python's standard library (e.g., `sqlite3`). No third-party packages like `pandas` or `networkx` are required or available.
- Do not modify the database schema or drop the index, as other legacy systems still depend on the file's current binary footprint.

Execute your script and ensure the output file `/home/user/top_type.txt` is created with the correct entity type.