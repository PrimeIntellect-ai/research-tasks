You are a build engineer managing a new artifact resolution system for our internal CI/CD pipeline. The system is designed to track build artifacts, their checksums, and their complex dependency graphs using a multi-service architecture (Redis for storage and a Python HTTP API for routing and resolution).

We have an initial skeleton of the system located in `/app/`. It consists of:
1. A Redis database (stores artifact metadata).
2. A Python API server (`/app/api.py`).

Your task is to complete the API implementation and write property-based tests to ensure the correctness of the dependency resolution and checksum validation logic.

**Requirements:**

1. **API Implementation (`/app/api.py`):**
   - The server must be a Python web server (e.g., using Flask or FastAPI) listening on `127.0.0.1:8080`.
   - Implement the route: `GET /api/v1/artifacts/resolve/<name>` with a required query parameter `version` (e.g., `?version=1.0.0`).
   - The API must query the local Redis server (running on `127.0.0.1:6379`).
   - Redis schema:
     - `artifact:<name>:<version>:deps` -> JSON string containing a list of objects: `[{"name": "libA", "version": "1.2"}, ...]`.
     - `artifact:<name>:<version>:checksum` -> String containing the SHA256 checksum of the artifact.
   - **Graph Traversal & Dependency Resolution:** The endpoint must recursively resolve all transitive dependencies for the requested artifact.
   - **Topological Sorting:** The resolved dependencies must be sorted topologically (dependencies must appear before the artifacts that depend on them). If there's a circular dependency, the API should return a `400 Bad Request` with `{"error": "circular dependency detected"}`.
   - **Aggregated Checksum:** Calculate a combined checksum for the resolved graph. This is defined as the SHA256 hash of the concatenated individual checksums in the exact topological order (including the root artifact's checksum at the very end).
   - **Success Response:** Return a `200 OK` JSON response:
     ```json
     {
       "artifact": "<name>",
       "version": "<version>",
       "resolved_dependencies": [{"name": "libA", "version": "1.2"}, ...],
       "aggregated_checksum": "<sha256_hex_string>"
     }
     ```

2. **Property-Based Testing (`/home/user/tests/test_graph.py`):**
   - Write a test suite using `pytest` and `hypothesis`.
   - Write property-based tests that generate random Directed Acyclic Graphs (DAGs) representing dependencies.
   - Assert that your topological sort implementation always places dependencies before their dependents.
   - Assert that the aggregated checksum correctly changes if any single node's checksum is mutated.
   - You can extract your graph traversal and checksum logic into a separate module (e.g., `/app/resolver.py`) to test it in isolation without needing Redis or HTTP requests.

3. **Service Orchestration:**
   - There is a script at `/app/start_services.sh` which starts the Redis server and the Python API. Ensure that by the end of your task, running this script successfully brings up both services, and the API correctly serves the HTTP endpoint.
   - Update `/app/start_services.sh` if necessary to ensure it uses the correct commands to start your Python server in the background.

Use whatever standard Python web and Redis libraries you prefer (e.g., `pip install flask redis hypothesis pytest`). Ensure your final services are running and listening on the expected ports.