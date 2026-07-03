You are a Database Reliability Engineer (DBRE) investigating a data corruption issue in a local multi-service application. 

The application consists of a Flask API backend and an Nginx reverse proxy. Recently, the production SQLite database (`/home/user/data/prod.db`) suffered an index corruption issue that causes its recursive queries to return stale, cyclic dependency data instead of a strict Directed Acyclic Graph (DAG). 

Your task consists of three parts:

**Part 1: Restore Service Routing**
The startup script `/app/start.sh` launches Flask on port 5000 and Nginx on port 8080. However, the Nginx configuration at `/home/user/nginx/nginx.conf` is missing the correct `proxy_pass` directive. Edit the Nginx configuration so that all requests to `http://127.0.0.1:8080/api/` are correctly routed to the Flask application at `127.0.0.1:5000`. After fixing the config, restart Nginx using the local config. Modify `/home/user/api/app.py` so that it connects to the uncorrupted backup database at `/home/user/data/backup.db` instead of `prod.db`.

**Part 2: Export the Uncorrupted Graph**
Using Python, write a script `/home/user/export_graph.py` that connects to `/home/user/data/backup.db`. 
- Reverse engineer the schema of the `dependencies` table (which represents parent-child relationships).
- Write a parameterized recursive CTE to extract the entire dependency tree starting from the node with `name = 'root_node'`.
- Export the resulting graph (all reachable nodes and their edges) to a JSON file at `/home/user/exported_graph.json`. Format the JSON as a list of dictionaries with keys `parent` and `child`.

**Part 3: Build a Graph Corruption Detector**
To prevent bad data from entering the system again, write a Python CLI tool at `/home/user/detect_corruption.py`.
- It must take a directory path as a command-line argument (e.g., `python3 /home/user/detect_corruption.py /path/to/corpus`).
- It must read all `.json` files in that directory (which follow the same format you exported).
- It must perform graph analytics to detect if the dependency graph contains any **cycles** (which indicates a corrupted index returning stale rows).
- For each file, print exactly `<filename>: CLEAN` if it is a valid DAG, or `<filename>: EVIL` if it contains a cycle.

Ensure all scripts are executable and output exactly as requested.