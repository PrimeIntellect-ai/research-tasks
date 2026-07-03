You are a data analyst tasked with building a microservice to analyze a network graph provided as a CSV file. 

You have been provided with an image at `/app/target_node.png` which contains the text of a specific "target node" ID you need to analyze. 
You also have a CSV file at `/app/network.csv` containing a directed graph with headers `src` and `dst`.

Your objective is to write and run a Rust HTTP server that serves graph analytics queries based on this data. 
Specifically, you must:
1. Extract the target node ID from the image `/app/target_node.png` (you can use tools like `tesseract` which are available in the system).
2. Create a Rust project in `/app/graph_service` and implement an HTTP server listening on `127.0.0.1:8080`.
3. The server must expose a single `GET` endpoint: `/reachable?depth=X`, where `X` is an integer.
4. When queried, the endpoint must calculate all nodes reachable from the extracted target node in **up to `X` steps** (directed edges only). Depth 0 means just the target node itself.
5. The endpoint should return a JSON array of these reachable node IDs as strings, sorted lexicographically. For example: `["N-1000", "N-2000", "N-8392"]`.
6. You may use any Rust crates you like (e.g., `axum`, `actix-web`, `rusqlite` for recursive CTEs, or simply purely in-memory structures).
7. Start your server in the background so that it is running and ready to accept requests.

Ensure your service handles the exact node string found in the image and traverses the graph correctly.