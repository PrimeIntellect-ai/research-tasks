You are a Database Reliability Engineer taking over a legacy infrastructure. We lost the documentation for our backup replication topology, but we have a video recording of the backup system's configuration diagnostic tool running in a terminal.

Your task is to rebuild the schema, run graph analytics to find our most critical bottlenecks, and expose this via an HTTP API for our internal dashboard.

Phase 1: Extraction
We have a video file at `/app/backup_topology.mp4`. This video scrolls through the backup replication links in the format: `REPLICATE: <source_db> -> <target_db>`. 
Extract the frames, read the text (you may need to install standard tools like `tesseract-ocr` and `ffmpeg`), and build a complete list of unique directed edges representing the database replication graph. 

Phase 2: Analytics
Using Python, load this graph and calculate the **Out-Degree Centrality** of each node (which represents how many downstream databases rely on it for backups). 

Phase 3: API Service
Create a Python HTTP API server (using any lightweight framework like Flask or FastAPI) running on `127.0.0.1:9090`. The server must accept a Bearer token `DBRE-SEC-991` in the `Authorization` header.

It must expose the following endpoints:
1. `GET /critical_nodes`
   - Query parameters: `limit` (integer, default 10), `offset` (integer, default 0), `min_centrality` (float, default 0.0)
   - Must return a JSON array of objects: `[{"node": "db_name", "centrality": 0.45}, ...]`
   - Must be sorted by centrality descending, then by node name alphabetically. 
   - Must correctly apply the pagination (`limit`, `offset`) and filter (`min_centrality`).

2. `GET /backup_chain/<node_name>`
   - Must return a JSON array of all downstream nodes that can be reached from `<node_name>` through the directed graph (i.e., the transitive closure of backups). 
   - The array must be sorted alphabetically.

Leave the server running in the background so it can be verified. Write the PID of your server to `/home/user/api.pid`.