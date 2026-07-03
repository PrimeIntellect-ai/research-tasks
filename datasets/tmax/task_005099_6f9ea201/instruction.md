You are an AI assistant helping a data researcher organize and serve a dataset of researcher collaborations.

We have a two-part task. First, we need to process raw data into a normalized graph using SQL. Second, we need to serve this graph via a custom asynchronous Python server that handles concurrent transaction updates, using a vendored library that currently has a critical bug.

### Step 1: Data Preparation
You will find raw CSV data in `/home/user/raw_data/` (you will need to create this for your own testing, assume the real evaluation environment has it).
The files are:
1. `nodes.csv` (columns: `node_id`, `researcher_name`)
2. `edges.csv` (columns: `source_id`, `target_id`, `raw_collaborations`)

Write a Python script that uses `sqlite3` to:
1. Load these CSVs into an in-memory SQLite database.
2. Write a SQL query using window functions to calculate a `normalized_weight` for each edge. The `normalized_weight` should be calculated as `raw_collaborations / MAX(raw_collaborations) OVER (PARTITION BY source_id)`.
3. Export the processed graph to `/home/user/processed_graph.json`.
The output schema must be EXACTLY:
```json
{
  "nodes": [{"id": 1, "name": "Alice"}, ...],
  "edges": [{"source": 1, "target": 2, "weight": 0.5}, ...]
}
```

### Step 2: Fix the Vendored Package
We are using a vendored package located at `/app/graph_transaction_lib` to manage in-memory graph transactions.
However, there is a known concurrency bug: when two requests attempt to update the edge between Node A and Node B in opposite directions simultaneously, the server deadlocks. 
Diagnose the locking mechanism inside `/app/graph_transaction_lib/graph_transaction_lib/locks.py` and fix the perturbation so that concurrent edge updates never deadlock.

### Step 3: Implement the API Server
Write a Python HTTP server using `aiohttp` or standard `asyncio` + `http.server` (running on `0.0.0.0:8080`).
The server must load `/home/user/processed_graph.json` using the fixed `graph_transaction_lib`.

Expose two endpoints:
1. `GET /shortest_path?src=<id>&dst=<id>`: 
   Returns `{"path": [src, ..., dst], "total_weight": <float>}`. Compute the shortest path using Dijkstra's algorithm based on the `weight` field.
2. `POST /update_edge`: 
   Accepts JSON `{"source": <id>, "target": <id>, "weight": <float>}`.
   Updates the graph using the vendored library's `ThreadSafeGraph.update_edge(src, dst, weight)` method. Return HTTP 200 `{"status": "ok"}`.

Start your server as a background process and leave it running. We will test it by sending concurrent `POST` requests and validating the `GET` endpoint.