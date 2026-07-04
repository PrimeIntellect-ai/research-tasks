You are a QA Engineer setting up a localized test environment to mock a legacy data-processing telemetry backend. 

Your objective is to create a mock REST API in Rust, configure a reverse proxy to route traffic to it, and process a test request.

Step 1: The Rust Mock API
Create a new Rust project in `/home/user/qa_mock`. The service must:
- Listen on `127.0.0.1:3000`.
- Expose a `POST /encode` endpoint.
- Accept a JSON payload with the schema: `{"text": "<string>", "shift": <integer>}`.
- Process the `text` field by applying a Caesar cipher shift (shifting English alphabet characters forward by `shift` places, preserving case, and leaving non-alphabetical characters unmodified).
- Apply Base64 encoding to the resulting shifted string.
- Return a JSON response with the schema: `{"result": "<base64_encoded_string>"}`.
- You may use any necessary standard or community crates (e.g., `serde`, `serde_json`, `axum`, `tiny_http`, `base64`). Start the service in the background.

Step 2: The Reverse Proxy
The frontend application expects to talk to a legacy endpoint via a reverse proxy. 
- Create an Nginx configuration file at `/home/user/nginx.conf`.
- Configure Nginx to listen on `127.0.0.1:8080`.
- Proxy all requests from `POST /v1/telemetry` to the Rust API at `http://127.0.0.1:3000/encode`.
- Since you do not have root access, ensure your Nginx configuration specifies local, user-writable directories for its `pid`, logs, and temporary paths (e.g., in `/home/user/nginx_temp/`).
- Start Nginx in the background using your configuration.

Step 3: Verification
Once both services are running, test the setup by sending the following exact payload to the Nginx reverse proxy using `curl`:
`{"text": "Project-X: Defend The Core!", "shift": 7}`

Save the exact HTTP response body (just the JSON output) from this `curl` command to `/home/user/test_result.json`. Leave both the Nginx and Rust processes running in the background.