You are acting as a database administrator and optimization engineer. We have a daily batch job that projects a friendship graph and calculates "second-degree influence" for every user, but the current Python prototype is too slow for our production pipeline. We need you to reimplement this graph query efficiently in Rust.

The raw graph data is located at `/home/user/edges.csv`. It contains two columns, `source` and `target`, representing undirected friendship edges between users (represented as integer IDs). 

Your task is to:
1. Initialize a new Rust project at `/home/user/influencer_calc`. You may use the `petgraph` or `csv` crates if you wish.
2. Write an optimized Rust program that reads `/home/user/edges.csv`.
3. Construct an undirected graph.
4. For every node, calculate its "second-degree influence". We define this strictly as the number of unique nodes that are exactly at distance 2 from the starting node. (A node is at distance 2 if it is a friend of a friend, but is NOT the node itself, and is NOT a direct friend of the node).
5. Find the top 5 nodes with the highest second-degree influence. If there is a tie in the count, break the tie by sorting by the node ID in ascending order.
6. Write the top 5 results to `/home/user/result.json` as a JSON array of arrays, e.g., `[[node_id, count], [node_id, count], ...]`.

Make sure your Rust program compiles and runs successfully, and generates the exact JSON file required.