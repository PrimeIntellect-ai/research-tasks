You are a Database Reliability Engineer (DBRE) responsible for managing a large fleet of database clusters. You need to analyze the backup metadata to optimize storage, identify critical single points of failure in incremental backup chains, and expose these insights via an internal HTTP API.

You have been provided with a local backup metadata snapshot located at `/app/data/backups.json`. This file contains a list of backup nodes (each with properties like `backup_id`, `region`, `size_mb`, `timestamp`) and edges indicating dependencies (e.g., an incremental backup depends on a previous snapshot).

Additionally, there is a proprietary internal package used for parsing and analyzing this graph, pre-vendored at `/app/backup_graph_lib-1.0.0`. 

However, the automated deployment failed because this package is broken. Your tasks are:

1. **Fix and Install the Vendored Package:**
   Navigate to `/app/backup_graph_lib-1.0.0`. There is a deliberate configuration error preventing it from being installed. Identify the error, fix it, and install the package into your Python environment. Note: You do not have internet access to download new external dependencies outside of standard ones already available or cached; fix the typographical error so it resolves to the correct standard library/installed package.

2. **Implement the Backup Analysis Service:**
   Write a Python HTTP server (using `Flask`, `FastAPI`, or the standard `http.server`) that listens on `127.0.0.1:8080`. 

   The service must implement the following endpoints:
   - `GET /health`: Returns `{"status": "ok"}`
   - `GET /critical_nodes`: Uses graph centrality algorithms (via the fixed package or `networkx`) to find the top 3 most depended-upon base backups (nodes with the highest in-degree). Returns `{"critical_nodes": ["id1", "id2", "id3"]}`.
   - `GET /window_top_backups`: Simulates a window function to partition the backups by `region`, ordering them by `size_mb` descending, and returning the top 2 largest backups per region. Returns `{"top_backups": {"regionA": ["idX", "idY"], "regionB": [...]}}`.
   - `POST /aggregate`: Accepts a JSON payload representing a NoSQL-like aggregation pipeline (e.g., `{"match": {"region": "us-east"}, "sum": "size_mb"}`). The service should process this aggregation against the NoSQL JSON data and return `{"result": <integer_sum>}`.

3. **Authentication:**
   All endpoints (except `/health`) must require HTTP Bearer authentication. Read the required secret token from `/app/config/auth_token.txt`. Reject unauthorized requests with a 401 status code.

Once your script is written, run it in the background so it continuously listens on the required port. Write a log file at `/home/user/service.log` capturing standard output from your server.