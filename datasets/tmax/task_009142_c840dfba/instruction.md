You are stepping in as a Database Administrator for a legacy system. We have an undocumented SQLite database located at `/home/user/sys_graph.db` that stores a complex network of system dependencies. 

Your goals are:
1. Reverse engineer the schema of the database to identify which table holds the entities (nodes) and which holds the relationships (edges). The tables have obfuscated names.
2. The entity table contains a column for the entity name. The relationship table contains directed edges with a weight (cost) associated with them.
3. Write a query or script to compute the shortest path (the path with the minimum total weight) from the entity named "AlphaCore" to the entity named "OmegaRelay". 
4. Output the result to a file named `/home/user/path_result.txt`.

The output file `/home/user/path_result.txt` must be formatted exactly as follows:
Line 1: A comma-separated list of entity names representing the exact path from AlphaCore to OmegaRelay (e.g., AlphaCore,BetaNode,GammaHub,OmegaRelay).
Line 2: The total weight of this shortest path as an integer.

You may use `sqlite3` and any standard shell utilities to explore the database and compute the result.