You are an open-source maintainer reviewing a broken Pull Request. A contributor submitted a PR to add a "critical path" (longest path) numerical algorithm to our Graph Processing API. The contributor claims the unit tests pass locally, but our CI integration tests are failing. 

Upon initial inspection, the PR introduces three distinct problems:
1. **Reverse Proxy Configuration:** The integration tests hit an Nginx reverse proxy (listening on port 8080) which forwards requests to our Python Flask backend (port 5000). The proxy configuration for the new endpoint `/api/v1/graph/` is stripping query parameters (`start_node` and `end_node`), causing the backend to throw 400 Bad Request errors.
2. **Import Ordering/Registry Bug:** The backend uses a registry pattern to route numerical algorithms. Because of how the contributor structured the imports between `main.py` and `algorithms.py`, the `critical_path` algorithm fails to register when the app is launched via `main.py`, though it worked in their isolated unit tests.
3. **Incomplete Algorithm:** The PR author actually left the `critical_path` numerical algorithm implementation as a stub (`TODO`) in `algorithms.py`.

Your task is to fix the PR and ensure the integration tests pass. 

**Workspace Structure:**
`/home/user/workspace/`
  ├── `nginx.conf` (Nginx configuration file)
  ├── `run_services.sh` (Script to start Nginx and the Flask backend)
  ├── `app/`
  │    ├── `main.py` (Flask web application)
  │    ├── `algorithms.py` (Numerical algorithms and registry)
  │    └── `requirements.txt`
  └── `tests/`
       └── `test_integration.py` (Test suite hitting `http://localhost:8080`)

**Steps to complete:**
1. Fix `/home/user/workspace/nginx.conf` so that requests to `/api/v1/graph/` properly retain and forward query parameters to the upstream Flask server. (Nginx is run in a rootless configuration).
2. Resolve the import cycle / registry order issue in `app/main.py` and `app/algorithms.py` so the `critical_path` function is successfully registered under the key `"critical_path"` in the `ALGORITHM_REGISTRY`.
3. Implement the `critical_path` algorithm in `app/algorithms.py`. The function receives a Directed Acyclic Graph (DAG) represented as a dictionary of dictionaries: `{node: {neighbor: edge_weight}}`. It must return the maximum weight path length (numerical float) from `start_node` to `end_node`.
4. Start the services by running `bash /home/user/workspace/run_services.sh`.
5. Run the integration tests using `pytest /home/user/workspace/tests/test_integration.py > /home/user/workspace/test_results.log`.

The task is considered successful when the `/home/user/workspace/test_results.log` file is generated and shows all tests passing (0 failures).