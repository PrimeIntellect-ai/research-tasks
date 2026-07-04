You are acting as a Database Administrator. We have an internal microservice, `bash-sqlite-graph-api`, which performs hierarchical graph analytics on our primary SQLite database. The microservice accepts a node ID and calculates the total number of downstream descendants (a simple centrality/hierarchy metric) using a recursive SQL query.

Recently, the service has been failing. When multiple internal systems query the API at the same time, it deadlocks and completely hangs. Furthermore, the query execution plan is highly unoptimized; single queries take way too long because of full table scans during the recursive CTE execution.

The source code for the microservice has been vendored into your environment at `/app/bash-sqlite-graph-api`. The database it uses is located at `/app/data/graph.db`. 

Your tasks are to:
1. **Optimize the Database**: Analyze the query performed by the microservice (you can find the SQL in the vendored package) and create the necessary index in `/app/data/graph.db` to optimize the recursive graph traversal.
2. **Fix the Deadlock/Concurrency Bug**: Investigate the Bash wrapper script `run_api.sh` in the vendored package. It uses `socat` to serve the API but fails to handle concurrent connections, causing a backlog and deadlock. Modify the script so it can process concurrent requests safely.
3. **Run the Service**: Start the fixed API service so that it listens on TCP port `8888` on `127.0.0.1`. Leave it running in the background.

The API must accept a simple TCP text stream containing a single Node ID (e.g., `10`) followed by a newline, and return the total count of descendant nodes followed by a newline.

Fix the package, optimize the database query plan by adding the proper index, and ensure the service is running and ready to handle concurrent queries.