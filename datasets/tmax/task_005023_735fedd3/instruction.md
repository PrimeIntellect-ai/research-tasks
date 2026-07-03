You are stepping into the role of a Database Administrator and Backend Engineer. We have a legacy system that logs network graph topology changes (edges and weights) as a subtitle track embedded within a video file. We also have a Go-based HTTP service that is supposed to serve 2-hop pathfinding queries based on this data, but it is currently returning massive, incorrect result sets due to a poorly written SQL query.

Your objectives:

1. **Extract and Materialize Graph Data**
   - We have provided a video file at `/app/network_topology.mp4`. The video contains a subtitle stream (Stream #0:1) with plain text data.
   - Extract this subtitle text stream using `ffmpeg`. 
   - The text contains graph edges in the format: `Source,Target,Weight` (e.g., `NodeA,NodeB,15`). Clean up any subtitle timing artifacts (like `00:00:01,000 --> ...` or sequence numbers) so you only have the raw CSV data.
   - Create an SQLite database at `/app/graph.db` with a table named `edges` (`source TEXT, target TEXT, weight INTEGER`).
   - Import the cleaned CSV data into this table.
   - **Query Optimization:** Create appropriate indexes on the `edges` table so that filtering by `source` and `target` is highly optimized.

2. **Fix and Deploy the Go Service**
   - The application code is located at `/app/server.go` (you need to create it based on the requirements below).
   - The server must listen on `127.0.0.1:8080`.
   - Implement an HTTP GET endpoint at `/api/two-hop`.
   - The endpoint must require an `Authorization` header with the exact value: `Bearer graph-admin-token`. Return HTTP 401 if unauthorized.
   - The endpoint will receive two query parameters: `start` and `end`.
   - **The Bug Context:** A previous developer tried to write a query to find all 2-hop paths from `start` to `end` and their total weight, but wrote an implicit cross join: `SELECT e1.source, e2.target, e1.weight + e2.weight FROM edges e1, edges e2 WHERE e1.source = ? AND e2.target = ?`. This returns garbage data because it doesn't enforce that the middle nodes connect!
   - **Your Fix:** Write a parameterized SQL query that correctly joins the graph on the middle node (i.e., `e1.target = e2.source`).
   - The endpoint should return a JSON array of objects representing all valid 2-hop paths between the `start` node and `end` node, ordered by total weight ascending. 
   - JSON response format must strictly be: `[{"path": "StartNode->MiddleNode->EndNode", "total_weight": 20}, ...]`
   - Build and run the Go server in the background so it is actively serving requests.

To complete the task: Ensure the SQLite database is created and fully populated at `/app/graph.db`, the indexes are built, and the fixed Go server is running on port 8080 and requires the auth token.