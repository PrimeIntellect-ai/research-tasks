You are a database administrator acting as a backend engineer for a telecommunications network. We have received an automated emergency voicemail, and our automated routing system is down. 

Your task is to build a new Go-based routing optimization API that queries our network database to find the hierarchical routing path for a given node.

Step 1: The voicemail is located at `/app/voicemail.wav`. Transcribe this audio file to extract the secret emergency authorization passphrase. 

Step 2: Examine the SQLite database at `/app/routing.sqlite`. You will need to reverse engineer its schema. It contains network nodes and their hierarchical relationships (edges). 

Step 3: Write a Go HTTP web service. The service must:
- Listen on `127.0.0.1:9090`.
- Expose a `POST /api/v1/route-to-root` endpoint.
- Require an `Authorization: Bearer <passphrase>` header, where `<passphrase>` is the exact phrase spoken in the audio file (in lowercase, spaces separating words). Return HTTP 401 if unauthorized.
- Accept a JSON request body in the format: `{"target_node": <int>}`.
- Query the SQLite database using an optimized recursive strategy (e.g., a Recursive CTE) to find the hierarchical path from the `target_node` up to the root node (the node with no parent).
- Return a JSON response with the path: `{"path": [target_node, parent_node, grandparent_node, ..., root_node]}`. Return HTTP 404 if the node does not exist.

Ensure your Go application handles errors gracefully and builds successfully. Keep the server running in the foreground or background so it can be tested. You may use standard Go libraries or the `github.com/mattn/go-sqlite3` driver.