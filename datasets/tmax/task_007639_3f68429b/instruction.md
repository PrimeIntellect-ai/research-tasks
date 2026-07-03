You are a data engineer building an ETL pipeline to analyze a hierarchical network structure. 

We have a SQLite database located at `/home/user/network.db`. It contains a single table `connections(source INT, target INT)` representing a directed graph of network nodes.

Your task is to write a C program that extracts a specific subgraph, calculates a centrality metric (out-degree), and exports the results.

Create a C program at `/home/user/extract_subgraph.c` that fulfills these requirements:
1. It takes exactly one command-line argument: an integer representing the `start_node`.
2. It connects to the `/home/user/network.db` SQLite database.
3. It uses a **parameterized SQL query** with a **recursive Common Table Expression (CTE)** to find all unique nodes that are reachable from the `start_node` (including the `start_node` itself).
4. For each reachable node, it calculates the node's out-degree (the total number of outgoing connections it has in the *entire* `connections` table, regardless of whether the targets are in the reachable set).
5. It exports the results to a CSV file at `/home/user/out_degrees.csv`. 
   - The first line must be the header: `node,out_degree`
   - Subsequent lines must list the reachable nodes and their out-degrees.
   - The results must be sorted by `out_degree` in descending order. In case of a tie, sort by `node` in ascending order.

Compile your program to `/home/user/extract_subgraph` (make sure to link the sqlite3 library). 
Finally, execute your program with `start_node` set to `1`.

Note: You may need to install the SQLite C development headers if they are not already present on the system.