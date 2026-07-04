You are tasked with fixing and deploying a custom graph analytics service for processing CSV datasets. We have a pre-vendored graph engine located at `/app/simple_graph/` which loads node and edge data from CSV files into an in-memory SQLite database and serves graph queries over HTTP.

However, the application has a few critical issues:
1. **Implicit Cross Join Bug**: The graph traversal logic in `/app/simple_graph/engine.py` contains a SQL query that fetches the neighbors of a node. It currently returns wildly incorrect results because of an implicit cross join in the SQL statement. You must identify and fix this SQL query so that it only returns the direct neighbors (i.e., `target_id` from the edges table where `source_id` matches the queried node).
2. **Missing Index**: Graph traversal is currently very slow because the edges table lacks an appropriate index. You must modify `/app/simple_graph/engine.py` to create an index on the `source_id` column of the `edges` table during the database initialization step.
3. **Start the Service**: Once the code is fixed, start the HTTP graph service on port `8080`.

The provided CSV files are located at `/data/nodes.csv` and `/data/edges.csv`.

To run the server, use:
`python3 /app/simple_graph/server.py --port 8080 --nodes /data/nodes.csv --edges /data/edges.csv`

The server exposes the following endpoint, which must work correctly after your fixes:
- `GET /shortest_path?src=<id>&dst=<id>`: Returns a JSON object `{"path": ["src", ..., "dst"]}` representing the shortest path.

Leave the server running in the background when you are done. The automated verifier will make HTTP requests to `http://localhost:8080/shortest_path` to verify the correctness and performance of your fixes.