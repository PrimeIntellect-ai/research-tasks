You are a data engineer troubleshooting a broken ETL pipeline that processes network routing graphs. The pipeline feeds from a local SQLite database, but downstream graph centrality metrics have been coming up incorrect due to stale data. 

Your investigation has revealed two things:
1. The original schema documentation was lost, but a screenshot of the schema whiteboard remains at `/app/network_schema.png`.
2. The SQLite database at `/home/user/pipeline.db` has a corrupted index named `idx_stale`. This index is causing queries to return stale or missing rows.

Your task is to fix the data extraction and serve the corrected graph metrics.

Perform the following steps:
1. **Reverse Engineer the Schema**: Use OCR on `/app/network_schema.png` to determine the name of the edge-list table and its source/destination column names. 
2. **Fix the Database**: Connect to `/home/user/pipeline.db` and resolve the corrupted index issue by dropping `idx_stale` so that full table scans or new indexes return the accurate data.
3. **Compute Graph Metrics**: Extract the edge data. Using Bash and standard CLI tools, calculate the unweighted in-degree (number of incoming edges) and out-degree (number of outgoing edges) for every node in the graph.
4. **Serve the Results**: Create and run a TCP server using ONLY Bash (e.g., using `nc` or `socat` in a loop) listening on `127.0.0.1:8888`. 
    - The server must accept a raw TCP connection.
    - The client will send a single node ID string followed by a newline (e.g., `NodeA\n`).
    - The server must respond with the precise string `IN:<in_degree>,OUT:<out_degree>\n` (e.g., `IN:5,OUT:2\n`) and then close the connection.
    - If the node does not exist, return `IN:0,OUT:0\n`.
    - Keep the server running in the background so it can process multiple sequential queries.

Do not use Python or Node.js for the server; you must implement the TCP server loop using Bash and standard Linux utilities.