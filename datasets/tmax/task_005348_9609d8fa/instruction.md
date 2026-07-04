You are a database administrator tasked with investigating a network intrusion and optimizing our forensic querying tools.

We have captured a video of the attack visualization at `/app/infection_map.mp4`. At exactly the 3-second mark, the visualization explicitly highlights the "Patient Zero" node ID in plain black-on-white text. 
We also have a SQLite database at `/app/network.db` containing a single table: `edges(parent_id TEXT, child_id TEXT)`. This table represents directional network connections.

There is a flawed API script at `/home/user/api.py`. It is meant to serve an endpoint `/trace?start_node=<id>` that recursively queries the database to find all downstream infected nodes starting from the given node, returning them as a JSON list. However, the current implementation uses a recursive Common Table Expression (CTE) with a severe implicit cross-join bug, causing it to return incorrect, massively duplicated results.

Your objectives:
1. Use `ffmpeg` and OCR (e.g., `tesseract`) to analyze `/app/infection_map.mp4` and identify the Patient Zero node ID.
2. Fix the recursive CTE in `/home/user/api.py`. It must correctly traverse the hierarchy from `parent_id` to `child_id` without cross-joining, returning a deduplicated list of all reachable nodes (including the start node) in any valid traversal order. Use parameterized queries to prevent SQL injection.
3. Update the API script to enforce an authorization header: `Authorization: Bearer db-admin-token`. Requests without this exact token should return a 401 status code.
4. The `/trace` endpoint must export the results as JSON in exactly this format: `{"infected_nodes": ["NODE_A", "NODE_B", ...]}`.
5. Start the web service. It must listen continuously on `127.0.0.1:8000`. Leave the server running in the background when you are finished.

Do not change the database schema. Ensure your API relies strictly on the SQLite database for its results.