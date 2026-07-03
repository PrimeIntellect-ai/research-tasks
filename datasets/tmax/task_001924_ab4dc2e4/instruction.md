You are a Database Reliability Engineer. Our team manages graph database backups by dumping them into relational SQLite databases. We have an automated validation service that extracts the graph from the SQLite backup, calculates key graph analytics, and compares them against known baselines. 

However, the current extraction pipeline is failing. The SQL query used to reconstruct the graph has a critical bug involving an implicit cross join, causing edge explosions and out-of-memory errors. Furthermore, the queries are unoptimized and unparameterized.

Your task is to fix the query, optimize the database, and implement a robust validation API service.

**System State & Provided Resources:**
- A SQLite database is located at `/home/user/backup.db`. 
  - Tables: `nodes(id TEXT, backup_id INTEGER)`, `edges(source_id TEXT, target_id TEXT, backup_id INTEGER)`.
- A stripped, compiled oracle binary is located at `/app/backup_oracle`. This binary correctly implements the graph analytics verification logic. If you run `/app/backup_oracle /home/user/backup.db <backup_id>`, it will output the correct JSON graph metrics (highest degree centrality node and average clustering coefficient). You can use it to verify your implementation.
- An initial, buggy SQL script is at `/home/user/extract_graph.sql`. It currently performs an implicit cross join.

**Your Objectives:**

1. **Database Optimization & Query Fix:**
   - Modify `/home/user/backup.db` by designing and applying an indexing strategy to efficiently query nodes and edges by `backup_id`.
   - Fix `/home/user/extract_graph.sql` so it correctly retrieves the edges for a specific `backup_id` without implicit cross joins. The query must be parameterized.

2. **Validation Service Implementation:**
   - Create an HTTP API server in Python or Node.js.
   - The service must bind to `127.0.0.1:8080`.
   - It must implement a `POST /validate` endpoint.
   - The endpoint will receive a JSON payload: `{"backup_id": <integer>}`.
   - When called, the service must:
     a) Use your fixed, parameterized query to extract all nodes and edges for the given `backup_id`.
     b) Construct an undirected graph.
     c) Calculate the node with the highest degree centrality. (If there is a tie, pick the node with the lexicographically smallest ID).
     d) Calculate the average clustering coefficient of the graph (rounded to 4 decimal places).
     e) Return a JSON response exactly like the output of `/app/backup_oracle`:
        `{"backup_id": <integer>, "top_centrality_node": "<node_id>", "avg_clustering": <float>}`

3. **Service Execution:**
   - Start your service in the background so it is listening on `127.0.0.1:8080` when you complete the task.
   - Ensure all necessary dependencies (e.g., `networkx`, `fastapi`, `uvicorn`, `express`) are installed in your environment.

Leave the HTTP server running. An automated test will send protocol-level HTTP POST requests to `127.0.0.1:8080/validate` to verify your service.