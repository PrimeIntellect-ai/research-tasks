You are a data analyst building a graph querying tool to process large CSV datasets of user interactions.

You have been provided with a vendored Rust HTTP server package located at `/app/graph_engine_rs`. It is designed to read two CSV files (`nodes.csv` and `edges.csv`), construct an in-memory graph, and serve queries over HTTP. 

However, the package is currently broken:
1. **Compilation Issue:** The `Cargo.toml` has a missing or broken dependency block that prevents compilation.
2. **Logical Bug (Implicit Cross Join):** The function `build_adjacency` in `src/graph.rs` contains a severe bug. Due to a missing conditional check (an implicit cross join), it assigns every single edge to every single node. This results in incorrect graph traversal paths and wrong centrality metrics.
3. **Inefficiency:** Even if the condition were simply added, the current O(V * E) nested loop is too slow for large datasets. You must rewrite it to index the edges efficiently in O(E) time.

Your tasks:
1. Fix the build configuration in `/app/graph_engine_rs/Cargo.toml`.
2. Fix the logic in `src/graph.rs` to correctly and efficiently build the adjacency list (a directed graph where an edge from A to B only belongs to A's adjacency list).
3. The server takes two command-line arguments: the path to the nodes CSV and the edges CSV.
   Run the server using the data files located at:
   - `/home/user/data/nodes.csv`
   - `/home/user/data/edges.csv`
4. Ensure the server binds to and listens on exactly `0.0.0.0:8080`.

The server provides two endpoints that you must ensure are working properly:
- `GET /shortest_path?from=<id>&to=<id>`: Returns JSON `{"path": ["A", "B", ...]}`
- `GET /centrality?node=<id>`: Returns JSON `{"out_degree": <int>}`

Leave the server running in the background when you are finished.