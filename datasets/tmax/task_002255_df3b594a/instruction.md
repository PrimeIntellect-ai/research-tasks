A network researcher is organizing a dataset of network topologies and needs your help automating the retrieval of routing paths based on audio signals.

We have an SQLite database located at `/app/topology.db` containing `nodes` and `edges` tables. There is also an audio file at `/app/endpoints.wav` which contains exactly two DTMF (Dual-Tone Multi-Frequency) tones. These two digits represent the `source` node ID and the `target` node ID, respectively, for a routing query.

Your task:
1. Decode the two DTMF tones from `/app/endpoints.wav` to determine the source and target node IDs. (You may install standard Python libraries like `scipy` or `numpy` if needed).
2. Query the SQLite database to compute the shortest path between the source and target nodes using the `edges` table. 
   *Note: A researcher previously created a view named `vw_edges` for convenience, but it contains an implicit cross join that returns exponentially wrong results. Do not use this view; query the base `edges` table directly or project the graph manually in Python to find the shortest path.*
3. Create and start a Python HTTP server listening exactly on `127.0.0.1:8080`.
4. Your server must respond to `GET /path` requests with a `200 OK` status and a JSON payload containing the shortest path you found. The JSON output must strictly validate against this schema:
   `{"path": [source_id, intermediate_node_1, ..., target_id]}`

Keep the server running in the background or foreground so we can verify it.