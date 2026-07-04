You are a database administrator optimizing an analytical query pipeline for a custom NoSQL graph database. The database engine lacks built-in graph centrality algorithms, so queries currently export raw documents and process them inefficiently.

Your task is to write a highly efficient Python script that mimics an optimized NoSQL aggregation pipeline to calculate degree centrality (total connections: in-degree + out-degree) and chain it to a document lookup.

The database dump consists of two files:
1. `/home/user/data/edges.json` - Contains a list of edge documents representing directed connections between nodes. Format: `[{"src": "N1", "dst": "N2"}, ...]`
2. `/home/user/data/nodes.json` - Contains a key-value mapping of node IDs to their attributes. Format: `{"N1": {"name": "Alpha", "cluster": "C1"}, ...}`

Write a Python script at `/home/user/get_top_centrality.py` that:
1. Accepts a single command-line argument `K` (an integer parameter).
2. Reads the edges to calculate the total degree centrality (in-degree + out-degree) for every node.
3. Identifies the top `K` nodes with the highest degree centrality. If there is a tie in centrality, sort by the node ID in ascending alphabetical order.
4. Uses the resulting top `K` node IDs to query the `nodes.json` dataset (simulating query-to-pipeline chaining) to fetch their `name` and `cluster`.
5. Outputs the final result to `/home/user/result.json` as a JSON array of objects, strictly formatted as:
   `[{"node_id": "...", "degree_centrality": X, "name": "...", "cluster": "..."}, ...]`
   The array must be sorted by degree_centrality descending, then node_id ascending.

Ensure the script only uses standard Python libraries (e.g., `json`, `sys`, `collections`).