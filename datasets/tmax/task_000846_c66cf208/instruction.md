You are a data analyst setting up a graph query service for a logistics network. You have two CSV files in `/home/user/data/`:
1. `cities.csv` (columns: `city_id`, `name`, `region`)
2. `connections.csv` (columns: `from_id`, `to_id`, `cost`)

Your task is to build a multi-service architecture using Python, RDFLib, NetworkX, and Nginx that exposes graph querying and shortest-path capabilities.

Step 1: Graph Materialization
Write a Python script `/home/user/build_graph.py` that reads the CSV files and materializes an RDF graph. Save it as `/home/user/data/graph.ttl` in Turtle format. 
Use the namespace `http://example.org/logistics/`. 
Define entities as `http://example.org/logistics/City/<name>` and connections using a custom predicate `http://example.org/logistics/connectedTo` with the `cost` stored as an integer literal using `http://example.org/logistics/cost`.

Step 2: API Service
Write a FastAPI application in `/home/user/api.py` that runs on `127.0.0.1:8000` (using uvicorn). It must expose:
- `POST /sparql`: Accepts JSON like `{"query": "<SPARQL_QUERY>"}`. It must execute the raw SPARQL query against the loaded RDF graph and return the JSON serialized results.
- `GET /shortest-path?start=<CityName>&end=<CityName>`: 
  1. Executes a SPARQL query internally to project all cities and connections into a `networkx` Directed Graph.
  2. Uses Dijkstra's algorithm in `networkx` to compute the shortest path based on the `cost`.
  3. Returns `{"path": ["CityA", "CityX", "CityB"], "total_cost": 120}`.

Step 3: Nginx Gateway
Create an Nginx configuration at `/home/user/nginx.conf`. It must:
- Run as the current user (do not try to drop privileges to nobody/root).
- Listen on `127.0.0.1:8080`.
- Proxy all requests to `127.0.0.1:8000`.
- Protect the endpoints using HTTP Basic Authentication. Credentials should be user: `analyst`, password: `graph123`. Create the htpasswd file at `/home/user/.htpasswd`.

Start both the FastAPI service (in the background) and Nginx (`nginx -c /home/user/nginx.conf`).
Write a log file to `/home/user/service_status.log` containing "SERVICES READY" once everything is up and running.