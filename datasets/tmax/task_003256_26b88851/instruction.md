You are acting as a Database Administrator optimizing a graph-like dataset stored in a relational database. 

We have a knowledge graph backed by a SQLite database located at `/app/knowledge.db`. Currently, recursive graph traversals are extremely slow. The lead architect left an architecture diagram and optimization hint on the server before departing, located at `/app/schema_hint.png`.

Your task is to:
1. Analyze the image `/app/schema_hint.png` (using OCR tools like `tesseract` which is pre-installed) to extract the hidden schema optimization hint.
2. Apply the necessary index creations or schema modifications to `/app/knowledge.db` as instructed in the image to optimize graph query plans.
3. Write and run a Python HTTP server that exposes an API for graph traversal. 

The Python HTTP server must meet these specifications:
- Listen on `127.0.0.1:8080`.
- Expose a `GET` endpoint at `/api/traverse`.
- Accept three query parameters: `start_node` (string), `edge_label` (string), and `max_depth` (integer).
- Execute a query against `/app/knowledge.db` to find all distinct target nodes reachable from `start_node` following only edges of type `edge_label` up to `max_depth` hops away. You must use a Recursive CTE (Common Table Expression) to perform this traversal efficiently.
- Return a JSON response in the exact format: `{"reachable_nodes": ["nodeA", "nodeB", ...], "count": 2}`. The list of reachable nodes must be sorted alphabetically.
- The server must handle requests concurrently and utilize the optimizations you applied to the database.

Start your server in the background so it remains running. Automated tests will verify your database schema changes and send real HTTP GET requests to your server to test the cross-representation mapping and query performance.