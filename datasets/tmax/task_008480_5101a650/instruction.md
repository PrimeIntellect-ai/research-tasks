You are a platform engineer responsible for maintaining a CI/CD pipeline for a data processing microservice. 

Currently, our data processing API (`/home/user/api/server.py`, written in Python using Flask) accepts POST requests at the `/process` endpoint. However, it lacks request validation and rate limiting, which has caused stability issues in production. 

Your task is to implement the missing features, write an end-to-end integration test suite in Node.js, and orchestrate the testing via a Bash script.

**Step 1: Update the API (`/home/user/api/server.py`)**
Modify the existing Flask application to include:
1. **Request Validation:** The `/process` endpoint must accept only JSON payloads. The JSON must contain a `batch_id` (string) and `records` (array). If the payload is not JSON, or is missing either of these fields, return an HTTP `400 Bad Request` status code.
2. **Rate Limiting:** Implement an in-memory rate limiter that restricts clients (based on IP address) to a maximum of `3 requests per 10 seconds` for the `/process` endpoint. If a client exceeds this limit, return an HTTP `429 Too Many Requests` status code.

*Note: You may modify `server.py` as needed, but it must continue to run with `python3 server.py` and listen on port `8080`.*

**Step 2: Write the E2E Test Suite (`/home/user/tests/e2e_test.js`)**
Create a Node.js script that tests the newly added features of the API running at `http://127.0.0.1:8080/process`. 
The script must perform the following test cases in order:
1. Send a POST request with valid JSON missing the `batch_id`. (Expect 400).
2. Send a POST request with valid JSON missing the `records`. (Expect 400).
3. Send 4 consecutive valid POST requests (containing both `batch_id` and `records`). 
   - The first 3 should return HTTP 200.
   - The 4th should return HTTP 429.

The Node.js script must evaluate these conditions and output a strict JSON file to `/home/user/test_report.json` with the following format:
```json
{
  "validation_passed": true,
  "rate_limit_passed": true
}
```
Set the booleans to `true` only if the respective tests behaved exactly as expected (returning the correct HTTP status codes).

**Step 3: Orchestrate the Pipeline (`/home/user/run_pipeline.sh`)**
Write a Bash script at `/home/user/run_pipeline.sh` that acts as the CI entrypoint. It must:
1. Start the Python API server in the background.
2. Wait for the server to become healthy/available.
3. Execute the Node.js test script (`node /home/user/tests/e2e_test.js`).
4. Gracefully terminate the Python API server process after the tests complete.
5. Exit with a status code of 0.

Ensure your Bash script is executable (`chmod +x`). All operations must happen within the `/home/user/` directory.