You are a mobile build engineer maintaining a new metadata routing pipeline. We need a robust, concurrent system to handle incoming build artifacts from various mobile CI nodes.

Please complete the following phases in `/home/user/workspace`:

1. **Package Management & Environment Setup:**
   - Create a Python virtual environment in `/home/user/workspace/venv`.
   - Install `Flask`, `requests`, `pytest`, and `hypothesis`.
   - Generate a `requirements.txt` in the workspace directory.

2. **Custom Data Structure (`build_tree.py`):**
   - Implement a Python class `BuildTree` that stores semantic versions of mobile builds.
   - Methods required:
     - `insert(platform: str, branch: str, version: str)` (e.g., `insert("ios", "main", "1.2.10")`). The version is always in `MAJOR.MINOR.PATCH` format.
     - `get_latest(platform: str, branch: str) -> str`: Returns the highest semantic version string for that platform and branch, or `None` if none exist.
   - Note: "1.2.10" is higher than "1.2.2".

3. **Property-Based Testing (`test_tree.py`):**
   - Write a test file using `pytest` and `hypothesis`.
   - Create a property-based test `test_highest_version_returned` that generates random valid semantic versions, inserts them into a `BuildTree` for a fixed platform/branch, and asserts that `get_latest` correctly returns the maximum version according to semantic versioning rules.

4. **Web Server (`server.py`):**
   - Write a Flask application running on `127.0.0.1:8080`.
   - It should maintain a global `BuildTree` instance.
   - Endpoint: `POST /add` with JSON payload `{"platform": "...", "branch": "...", "version": "..."}`. Returns 200 OK.
   - Endpoint: `GET /latest?platform=...&branch=...`. Returns JSON `{"version": "..."}`.

5. **Reverse Proxy Configuration (`nginx.conf`):**
   - Write a valid local Nginx configuration file at `/home/user/workspace/nginx.conf`.
   - It must listen on `127.0.0.1:9090` and proxy all requests to the Flask app on `8080`.
   - Do not use root privileges; ensure `pid`, `error_log`, and `client_body_temp_path` directives point to `/tmp/` or `/home/user/workspace/` so it can run as a standard user.

6. **Go Concurrency Fix (`uploader.go`):**
   - There is a Go script at `/home/user/workspace/uploader.go` that simulates CI nodes concurrently pushing metadata to `http://127.0.0.1:9090/add`.
   - It currently hangs due to a deadlock caused by improper channel usage/goroutine synchronization.
   - Fix the concurrency bug in `uploader.go`.
   - Compile it to `/home/user/workspace/uploader` and run it successfully.

After ensuring the server and proxy are running and the uploader successfully pushes all data, write the output of `curl http://127.0.0.1:9090/latest?platform=android&branch=release` to `/home/user/workspace/final_result.log`.