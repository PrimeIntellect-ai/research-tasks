You are a Data Analyst for a logistics company. You have been given a CSV file containing historical records of network routes at `/home/user/routes.csv`. 

Due to a bug in an old logging system, this CSV contains "stale" rows. Whenever a route's distance was updated, a new row was appended rather than updating the old one. Therefore, there can be multiple rows for the same `(source, target)` pair.

Your task is to:
1. Load the data from `/home/user/routes.csv` into a new SQLite database located at `/home/user/network.db`.
2. Write a SQL query or create a view that extracts only the *active* network. The active network consists of only the most recently updated row (maximum `last_updated` timestamp) for every unique `(source, target)` pair.
3. Using Python and the `networkx` library, build a directed graph from the active network.
4. Calculate the following metrics:
   - The total number of edges in the active network.
   - The shortest path from node `S` to node `T` minimizing the `distance` (weighted shortest path).
   - The total distance of that shortest path.
   - The top 3 nodes with the highest Betweenness Centrality. Calculate this using `networkx.betweenness_centrality` on the directed graph without passing a weight parameter (unweighted betweenness). If there are ties, order alphabetically.

Save your final results in a JSON file at `/home/user/analysis_result.json` with the exact following structure:
```json
{
    "active_edge_count": 0,
    "shortest_path_S_to_T": ["S", "X", "T"],
    "shortest_path_distance": 0.0,
    "top_3_betweenness_nodes": ["X", "Y", "Z"]
}
```

Constraints:
- You must create the SQLite database and perform the deduplication logic via SQL (e.g., using window functions, CTEs, or group bys).
- You may install `networkx` via pip if it is not present.
- Do not use absolute paths outside of `/home/user`.