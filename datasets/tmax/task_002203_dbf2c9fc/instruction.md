You are an integration developer responsible for building and testing a new security rule update API. The API is a WebSocket service that strictly validates semantic versions to prevent downgrade attacks. 

You need to implement the backend server, a property-based integration test suite, and a runner script. You must write the server in Node.js and the test client in Python, using bash to orchestrate them.

Create all files in the directory `/home/user/ws_api_test/`.

**Phase 1: The WebSocket Server (Node.js)**
Create a server script at `/home/user/ws_api_test/server.js`.
1. It must listen for WebSocket connections on `ws://localhost:8765`.
2. It should accept JSON payloads in the format: `{"action": "update", "version": "<semver_string>"}`.
3. Using the npm `semver` package, evaluate the `version`:
   - If the version is a valid semantic version AND is strictly greater than `2.0.0`, respond with the JSON string `{"status": "success"}`.
   - If the version is a valid semantic version but is less than or equal to `2.0.0`, respond with `{"status": "rejected"}`.
   - If the version is missing, not a string, or an invalid semantic version (e.g., `not-a-version`, `2.0.0.1`), respond with `{"status": "error"}`.

**Phase 2: The Integration Test Client (Python)**
Create a Python script at `/home/user/ws_api_test/test.py`.
1. Use the `websockets` library to connect to the Node.js server.
2. Implement a property-based test generator that dynamically creates exactly 13 test cases:
   - 5 randomly generated, valid semantic versions strictly greater than `2.0.0` (e.g., `3.1.4`, `2.0.1-alpha`).
   - 5 randomly generated, valid semantic versions strictly less than or equal to `2.0.0` (e.g., `1.9.9`, `2.0.0`).
   - 3 intentionally invalid semantic version strings.
3. Send each generated version to the server sequentially using the required JSON format.
4. Record the server's response for each test case.
5. Write the results to `/home/user/ws_api_test/test_report.log`. Each line must contain exactly the tested version string and the received status, separated by a comma. Format: `<version_string>,<status>` (e.g., `3.1.4,success`). Do not include extra spaces around the comma.

**Phase 3: The Runner Script (Bash)**
Create an executable bash script at `/home/user/ws_api_test/run_tests.sh` that automates the entire process:
1. Initializes a local Node.js environment and installs the `ws` and `semver` packages.
2. Creates a Python virtual environment, activates it, and installs the `websockets` and `packaging` (or `semver`) packages.
3. Starts the `server.js` in the background and waits for it to be ready to accept connections.
4. Runs `test.py`.
5. Gracefully kills the background Node.js server upon completion.

Your final outcome should be executing `/home/user/ws_api_test/run_tests.sh` to generate the `test_report.log` file.