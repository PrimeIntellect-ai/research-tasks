You are a database administrator tasked with optimizing a graph traversal operation for a network routing system. 

We have an SQLite database located at `/home/user/network.db` containing a table named `edges`. 
Recently, a buggy deployment caused "stale" records to be left in the database instead of being overwritten. There is an index on this table, but it is effectively corrupted for our purposes because it includes these stale rows.

The `edges` table has the following schema:
`id INTEGER PRIMARY KEY, src TEXT, dst TEXT, cost INTEGER, updated_at INTEGER`

Your objective is to write a C program that directly queries the database to find the shortest network path, bypassing the stale data using analytical SQL features.

Requirements:
1. Write a C program at `/home/user/router.c` that uses the `sqlite3` C library.
2. The program must connect to `/home/user/network.db`.
3. You must execute a single SQLite query (using `sqlite3_exec` or prepared statements) that does the following:
   - Filters out stale edges: For any given `(src, dst)` pair, only the edge with the highest `updated_at` value should be considered valid. (Use SQLite window functions for this).
   - Traverses the graph: Use a recursive Common Table Expression (`WITH RECURSIVE`) to find all valid paths starting from the node `'CORE_1'` and ending at the node `'EDGE_7'`.
   - Prevents infinite loops/cycles in the recursive query.
   - Calculates the total cost for each path and selects the single path with the lowest total cost.
4. The C program must output the result to a text file at `/home/user/optimal_route.txt`.
5. The output format in the text file must be strictly: `<path_string>,<total_cost>`.
   - Example format: `CORE_1->DIST_5->EDGE_7,42`
6. Compile your program using `gcc /home/user/router.c -o /home/user/router -lsqlite3`.
7. Execute your compiled program to generate the output file.

Ensure your query strictly evaluates only the latest records per edge pair before attempting the recursive shortest-path traversal.