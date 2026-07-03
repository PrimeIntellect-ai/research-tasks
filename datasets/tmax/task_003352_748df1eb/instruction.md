You are acting as a Database Administrator for a graph analytics platform.

We store our graph topology in a SQLite database located at `/home/user/graph.db`. A bash script at `/home/user/compute_metrics.sh` queries this database to calculate the out-degree centrality for all nodes and returns the top results. However, the script is currently returning incorrect, inflated centrality metrics because of an implicit cross join in the graph projection logic—a missing composite join key.

A previous engineer left a screenshot of the corrected data model diagram in `/app/schema_clue.png`. 

Your objectives are:
1. Analyze `/app/schema_clue.png` (using an OCR tool like `tesseract` which is pre-installed) to reverse-engineer the correct table relationship.
2. Fix the SQL query inside `/home/user/compute_metrics.sh`. The query must correctly compute the out-degree centrality (number of outgoing edges) for each node, accounting for the correct composite join keys to prevent duplication.
3. Modify `/home/user/compute_metrics.sh` so that instead of just printing to the console, it outputs exactly the top 3 nodes with the highest centrality in JSON format to `/home/user/top_nodes.json`. The JSON should be an array of objects: `[{"node_id": "...", "centrality": ...}, ...]`. If there is a tie, sort by `node_id` ascending.
4. Write and execute a Bash script at `/home/user/serve.sh` that brings up an HTTP server on port 8080. When a client makes a `GET` request to `http://127.0.0.1:8080/api/top_nodes`, the server must respond with a `200 OK` status, a `Content-Type: application/json` header, and the exact contents of `/home/user/top_nodes.json` as the response body. Ensure this server runs in the background so it can be verified.

Do not use anything other than standard Bash built-ins, SQLite, and core network utilities (like `nc` or `socat`) to serve the API.