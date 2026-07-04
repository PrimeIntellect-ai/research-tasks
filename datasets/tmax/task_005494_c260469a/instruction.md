You are a database administrator tasked with optimizing a slow, iterative graph traversal process. 

An existing C++ application currently queries a SQLite database (`/home/user/network.db`) in a naive, iterative loop to traverse a service dependency graph. Your goal is to optimize this by leveraging SQLite's Recursive Common Table Expressions (CTEs) to perform the hierarchical query entirely within the database engine, and then output the results via a C++ pipeline.

The database has a single table:
`edges (source TEXT, target TEXT)`

Your task:
1. Modify the C++ source file located at `/home/user/db_traversal.cpp`. It currently contains a placeholder for the SQL query and the execution logic.
2. Write a single optimized SQL query using a `WITH RECURSIVE` CTE to find all downstream dependencies of the node named `'Service_A'`. 
3. The query must compute the *shortest path distance* (depth) from `'Service_A'` to each dependent node. The depth of an immediate child of `'Service_A'` is 1.
4. If a node is reachable via multiple paths, only the shortest path depth should be returned.
5. Execute this query using the SQLite3 C API in the provided C++ file.
6. The C++ program must write the results to `/home/user/optimized_paths.log` in the following exact format, ordered alphabetically by the target node name:
`Node: <target_name>, Shortest Depth: <depth>`

For example:
Node: Service_B, Shortest Depth: 1
Node: Service_C, Shortest Depth: 2

You must compile the program using:
`g++ /home/user/db_traversal.cpp -lsqlite3 -o /home/user/db_traversal`

Run the compiled executable to generate the log file.