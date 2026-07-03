You are a data engineer building a graph processing ETL component. We need a lightweight HTTP service that accepts streaming graph edges and provides aggregation over the graph. We are using a vendored version of the `tinydb` library as our NoSQL backend.

However, the vendored `tinydb` library located at `/app/tinydb` has a deliberate perturbation: a recent unmerged patch introduced a locking issue that deadlocks concurrent inserts. 

Your task:
1. Fix the deadlock bug in the vendored `tinydb` library under `/app/tinydb`. The bug is somewhere in the storage locking logic when writing concurrent transactions. Install the library into your environment via `pip install -e /app/tinydb`.
2. Write a Python HTTP service using FastAPI (save it at `/app/main.py`) that listens on `0.0.0.0:8080`.
3. The service must implement the following endpoints:
   - `POST /edge`: Accepts a JSON payload matching the schema: `{"src": "string", "dst": "string", "weight": "integer"}`. It should store this edge in a TinyDB instance backed by a file at `/app/graph.json`.
   - `GET /aggregate`: Reads the stored edges from TinyDB and calculates the total outgoing weight (out-degree) for every source node. It must return a JSON list of objects, structured exactly as: `[{"node": "node_name", "out_degree": total_weight}, ...]`. The list must be sorted by `out_degree` descending, and then by `node` alphabetically ascending for ties.

Ensure your service handles concurrent POST requests smoothly (which requires your TinyDB fix). 
You must start the server in the background so it remains running. E.g., `uvicorn main:app --host 0.0.0.0 --port 8080 &`.

Your solution will be tested by an automated verifier that will:
- Send concurrent HTTP POST requests to `/edge` to insert a large graph.
- Check if any requests hang (deadlock).
- Call `/aggregate` and strictly validate the JSON output schema and calculated results.