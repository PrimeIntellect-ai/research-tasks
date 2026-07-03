You are a build engineer managing internal software artifacts. We need a lightweight, local Artifact Dependency Resolver API called `ArtifactoryLite` to manage build dependencies and compute build orders. 

Your task is to implement this system from scratch in Python, following these specific phases:

**Phase 1: Environment and Dependencies**
1. Create a project directory at `/home/user/workspace`.
2. Create a Python virtual environment at `/home/user/venv`.
3. Create a `/home/user/workspace/requirements.txt` file and install necessary packages to build a REST API (we recommend FastAPI or Flask), rate limiting tools (like `slowapi` or `Flask-Limiter`), and `pytest` for testing.

**Phase 2: Custom Data Structure (`/home/user/workspace/dag.py`)**
Implement a custom directed acyclic graph to manage dependencies. Create a class `ArtifactDAG` with:
- `add_artifact(name: str, version: str, deps: list[str])`: Adds an artifact to the graph. `deps` is a list of strings in the format `"name@version"`.
- `get_build_order(name: str, version: str) -> list[str]`: Computes the topological sort order required to build the artifact (dependencies must appear before the artifacts that depend on them). Returns a list of `"name@version"` strings.
- If `add_artifact` detects a cyclic dependency, it must raise a custom exception `CyclicDependencyError`.

**Phase 3: REST API (`/home/user/workspace/app.py`)**
Implement the API server. It must maintain an in-memory instance of `ArtifactDAG`.
- **Endpoint 1:** `POST /artifacts`
  - Accepts JSON: `{"name": "libA", "version": "1.0.0", "deps": ["libB@2.0.0"]}`
  - Adds the artifact to the DAG.
  - Returns HTTP 201 on success.
  - Returns HTTP 400 if a `CyclicDependencyError` is raised.
  - **Rate Limiting:** This endpoint must be strictly rate-limited to **10 requests per minute** per IP address. Exceeding this should return HTTP 429.
- **Endpoint 2:** `GET /resolve/{name}/{version}`
  - Returns HTTP 200 with JSON: `{"build_order": ["libB@2.0.0", "libA@1.0.0"]}`
  - Returns HTTP 404 if the artifact doesn't exist.

**Phase 4: Testing (`/home/user/workspace/test_app.py`)**
Write a `pytest` suite that includes:
- A fixture that initializes an empty `ArtifactDAG`.
- Tests verifying the topological sorting logic.
- Tests verifying that `CyclicDependencyError` is correctly raised for cycles.
- Mock-based tests verifying the API's rate limiting behavior (simulating >10 requests).

**Phase 5: Execution Script**
Create a bash script at `/home/user/start_server.sh` that, when executed, activates the virtual environment and starts the API server in the background on port `8080`. The script must exit cleanly (return 0) while leaving the server running.

**Constraints & Verification:**
- Use standard Python 3.
- The automated test will first run `pytest /home/user/workspace/test_app.py`.
- Then it will execute `/home/user/start_server.sh`.
- Finally, it will run standard `curl` commands against `http://localhost:8080` to verify correct topological sorting, cycle detection (400 response), and rate limiting (429 response).