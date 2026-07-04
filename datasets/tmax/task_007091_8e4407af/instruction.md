You are a database administrator optimizing a graph traversal query pipeline. A previous extraction job produced a graph edge list in `/home/user/network_edges.csv`, but it contains erroneous implicit cross joins (marked with the string `CROSS_JOIN_ERROR` in the third column) that are causing shortest-path queries to return invalid results (e.g., claiming 1-hop paths exist everywhere).

Your task:
1. Use a bash pipeline to filter `/home/user/network_edges.csv`, removing any lines containing the string `CROSS_JOIN_ERROR`. Save the cleaned file to `/home/user/cleaned_edges.csv`.
2. Write a Python script `/home/user/shortest_path.py` that reads `/home/user/cleaned_edges.csv`. The CSV has no header and contains three comma-separated columns: `source_node`, `target_node`, `edge_weight`.
3. The Python script must compute the shortest path distance (ignoring edge weights, just treating every edge as a distance of 1 hop) from `NODE_001` to `NODE_999`. The graph is directed (edges point from `source_node` to `target_node`).
4. The script should output the integer representing the minimum number of hops between `NODE_001` and `NODE_999` to a file located at `/home/user/result.txt`.

Ensure your Python script is executable and efficiently builds the graph using an adjacency list (or equivalent index strategy) before performing the traversal.