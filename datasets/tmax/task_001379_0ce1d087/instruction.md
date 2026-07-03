You are helping a developer organize a chaotic set of project files for a monorepo migration. We need to analyze the dependency graph of these modules, compute a numerical "Dependency Weight" for each, expose this data via a local web service, and route traffic to it through a reverse proxy.

Your workspace is `/home/user/workspace`. Inside `/home/user/workspace/projects`, there are several JSON files. Each file represents a project module and contains a dictionary with the keys: `module` (string), `cost` (integer), and `dependencies` (list of strings representing other module names).

Perform the following tasks:

1. **Dependency Analysis & Numerical Computation**:
   Write a Python script `/home/user/workspace/analyzer.py` that reads all the JSON files in the `projects` directory. It must compute the "Total Dependency Weight" ($W$) for each module.
   The formula is: 
   $W(m) = C(m) + \sum_{d \in D} (0.5 \times W(d))$
   where $C(m)$ is the base `cost` of module $m$, and $D$ is the list of its `dependencies`. 
   You can assume the dependency graph is a Directed Acyclic Graph (DAG).
   
   The script must serialize the results and save them to `/home/user/workspace/migration_order.json`. The output must be a JSON object mapping the `module` name to its float $W$ value (e.g., `{"auth": 27.5, "db": 25.0}`). 

2. **Web Service**:
   Extend `analyzer.py` so that when executed, it starts a simple HTTP server (using `http.server`, `Flask`, or `FastAPI`) listening on `127.0.0.1:8000`. 
   When a GET request is made to `/weights`, it must return the contents of `migration_order.json` with a `200 OK` status and `application/json` content type. Run this process in the background.

3. **Reverse Proxy Configuration**:
   Create an Nginx configuration file at `/home/user/workspace/nginx.conf`. Configure Nginx to act as a reverse proxy listening on `127.0.0.1:8080`. 
   It should proxy requests from `http://127.0.0.1:8080/api/weights` to `http://127.0.0.1:8000/weights`.
   *Note: Since you do not have root access, make sure your Nginx config writes its pid, access log, error log, and temp files to directories within `/home/user/workspace/nginx/` (which you should create), and start Nginx using your local config.*

4. **Unit Testing**:
   Write a unit test file `/home/user/workspace/test_analyzer.py` using `pytest`. Write at least two tests that import the computation logic from `analyzer.py` and verify that the weight calculation is correct for a simple mocked DAG. Leave a log of the test run at `/home/user/workspace/test_results.log`.

Make sure the web server and Nginx proxy are both running when you finish.