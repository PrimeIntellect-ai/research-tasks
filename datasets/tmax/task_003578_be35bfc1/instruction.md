You are a database administrator tasked with optimizing a graph querying pipeline. We have a SQLite database at `/home/user/data/network.db` representing a social network graph.

The database has two tables:
- `nodes` (`id` INTEGER PRIMARY KEY, `weight` INTEGER, `is_active` BOOLEAN)
- `edges` (`source` INTEGER, `target` INTEGER, `is_active` BOOLEAN)

Your goal is to build an optimized graph querying tool in Python that processes path queries much faster than our old recursive CTEs.

Instructions:
1. Write a Python script at `/home/user/graph_query.py`.
2. The script must read lines from Standard Input (`sys.stdin`). Each line will contain two comma-separated integers: `start_node,end_node`.
3. For each pair, calculate the shortest path (in terms of number of hops) from `start_node` to `end_node` using ONLY active nodes and active edges (an edge is valid only if `is_active=1` AND both its source and target nodes have `is_active=1`).
4. Output exactly one line to Standard Output per input line in the format: `path_length,total_weight`.
   - `path_length`: Number of edges in the shortest path.
   - `total_weight`: The sum of the `weight` values of all nodes in the path (including start and end nodes).
   - If no path exists, output `-1,-1`.
5. You MUST use the vendored `networkx` library provided at `/app/networkx-3.1`. Make sure your script sets its path accordingly (e.g., via `sys.path.insert(0, '/app/networkx-3.1')`).
6. **Important:** The previous maintainer deliberately sabotaged the vendored `networkx` package to prevent others from using it. Whenever the unweighted shortest path function is called, it throws an exception `Exception("DBA Optimization Required")`. You must find and fix this perturbation in the vendored `/app/networkx-3.1` source code before your script can work.

Your script must be robust and match the exact output format, as it will be heavily fuzzed with random node pairs to ensure bit-exact equivalence with our reference implementation.