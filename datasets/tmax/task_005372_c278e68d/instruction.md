You are a platform engineer maintaining CI/CD pipelines. We recently discovered a critical CVE in our WebSocket communication libraries that affects versions older than certain thresholds. To ensure our microservices are secure and functional, you need to write an end-to-end (E2E) security test orchestrator.

Your task is to write a script (in Python, Node.js, or Bash) that reads a list of service endpoints and their required minimum secure versions, queries each service over WebSockets, performs semantic version comparisons, and runs an E2E test on the secure ones.

**Requirements:**
1. Read the file `/home/user/endpoints.csv`. It contains a comma-separated list with headers: `endpoint,min_version`.
2. For each endpoint in the CSV, establish a WebSocket connection.
3. Once connected, send a JSON payload to request the server version:
   `{"cmd": "version"}`
4. The server will respond with a JSON object:
   `{"version": "X.Y.Z"}`
5. Parse this version and compare it against the `min_version` specified in the CSV using Semantic Versioning (SemVer) rules.
6. If the server's version is **less than** the `min_version`, mark its status as `"INSECURE"` and close the connection.
7. If the server's version is **greater than or equal to** the `min_version`, proceed to the E2E test by sending this JSON payload over the same connection:
   `{"cmd": "test", "auth": "e2e-token"}`
8. The server will respond with a JSON object containing a status:
   `{"status": "ok"}` or `{"status": "error"}`
9. If the status is `"ok"`, mark the endpoint as `"SECURE_PASS"`. If the status is anything else, mark it as `"SECURE_FAIL"`.
10. Finally, generate a JSON report file at `/home/user/security_report.json`. The file must contain a single JSON object mapping each endpoint URL to its final status string.

**Example Output Format for `/home/user/security_report.json`:**
```json
{
  "ws://localhost:9001": "INSECURE",
  "ws://localhost:9002": "SECURE_PASS",
  "ws://localhost:9003": "SECURE_FAIL"
}
```

The WebSocket servers are already running locally. You may install any necessary packages in your user environment (e.g., using `pip install --user` or `npm install`).