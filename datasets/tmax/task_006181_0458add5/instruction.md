You are a build engineer managing an artifact pipeline. We have a build orchestrator emitting artifact metadata over a WebSocket stream, but we need to process this data, expose the stream via a reverse proxy, and ensure our parsing logic is robustly tested.

Your tasks are to:

1. **Reverse Proxy Configuration:**
Create an unprivileged Nginx configuration file at `/home/user/nginx.conf`. 
- Nginx must listen on port `8090`.
- It must proxy all requests from `/stream` to the local WebSocket server running at `127.0.0.1:8080`.
- Make sure to configure Nginx to run as the current user (do not use `user root;`), and place the `pid`, `access_log`, and `error_log` files in `/home/user/`.
- Start nginx in the background using this configuration.

2. **WebSocket Client & Data Parsing:**
Write a Python script at `/home/user/client.py`.
- It should connect to the WebSocket via the reverse proxy (`ws://127.0.0.1:8090/stream`).
- The WebSocket server emits JSON payloads like: 
  `{"artifact_id": "build-123", "status": "failure", "metrics": {"size_bytes": 1024, "build_time_sec": 45.2}}`
- Your script must parse this incoming stream.
- It must implement a pure function `def parse_and_transform(json_str: str) -> str | None:` that parses the JSON string.
- If `status` is `"failure"`, the function should return a comma-separated string: `"<artifact_id>,<size_bytes>,<build_time_sec>"`. 
- If `status` is not `"failure"`, it should return `None`.
- For any `json.JSONDecodeError` or missing keys in the dictionary, it should return `None`.
- The script should continuously listen, call this function for each message, and if a string is returned, append it to `/home/user/failed_artifacts.log` (with a newline).

3. **Property-Based Testing:**
Write a test file at `/home/user/test_client.py` using `pytest` and `hypothesis`.
- Import `parse_and_transform` from `client`.
- Write a property-based test that generates arbitrary strings and ensures `parse_and_transform` either returns a string or `None`, but **never raises an unhandled exception** (like KeyError, TypeError, etc.).
- Run the test to verify it passes.

Leave the client running in the background so it processes the incoming data.

Note: The WebSocket server is already running on port 8080. You can install any required Python packages (like `websockets`, `pytest`, `hypothesis`) via `pip`.