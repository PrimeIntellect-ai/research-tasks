You are a database administrator tasked with fixing a performance issue. A previous admin attempted to write a SQL query to find the shortest path from a central server (`SYS_00`) to all other reachable servers in our network. However, their query suffered from an implicit cross join in the recursive CTE, leading to combinatorial explosion, infinite loops, and incorrect results.

Instead of debugging their broken SQL, we need you to write a clean, optimized script (in any language of your choice, e.g., Python, Ruby, Perl, or Bash) to process the raw exported data and output the correct paginated results.

The network topology has been exported to a CSV file at `/home/user/graph_edges.csv`.
The file has a header and three columns: `u,v,cost` representing directed edges from node `u` to node `v` with the given travel `cost`.

Your task:
1. Parse the network graph from `/home/user/graph_edges.csv`.
2. Compute the exact shortest path distance from the start node `SYS_00` to all other reachable nodes.
3. Exclude the start node (`SYS_00`) from your final results.
4. Sort the remaining reachable nodes primarily by their shortest path distance in **ascending** order, and secondarily by their node name in **ascending** alphabetical order.
5. Paginate the results: **Skip the first 5 results** (offset = 5) and **keep the next 5 results** (limit = 5).
6. Save these 5 results into a file named `/home/user/optimized_paths.csv`.

The output file `/home/user/optimized_paths.csv` must be formatted strictly as `node,cost` (without spaces, one per line) and should NOT include a header.

Example of expected output format:
SYS_98,7
SYS_12,8
...