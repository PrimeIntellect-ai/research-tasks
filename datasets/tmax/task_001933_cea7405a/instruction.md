You are a QA engineer tasked with replacing a flaky legacy hardware component in our CI/CD pipeline with a reliable Python-based mock service. 

We have an executable binary dumped from the legacy hardware located at `/app/legacy_calc`. This binary reads a specially encoded hexadecimal string from standard input, decodes it, performs a calculation, and outputs the result to standard output. 

Your task has three parts:

1. **Analyze the Binary**: 
   Reverse engineer or treat `/app/legacy_calc` as a black box to understand its encoding/decoding scheme and computation logic. (Hint: It expects a hex-encoded string on stdin).

2. **Implement the Emulator Server**:
   Write a Python HTTP server that accurately emulates the behavior of the legacy binary.
   - **Listen Address**: `127.0.0.1:9090`
   - **Endpoint**: `POST /api/v1/compute`
   - **Authentication**: Must require an `Authorization: Bearer secret-QA-8821` header. Reject unauthorized requests with a `401 Unauthorized` status.
   - **Request Format**: JSON body `{"data": "<hex_string>"}`
   - **Response Format**: JSON body `{"result": <integer_result>}`
   - **Validation**: If the payload is missing, not valid hex, or incorrectly formatted, return a `400 Bad Request`.
   - **Rate Limiting**: The legacy hardware was slow. Implement a rate limit of exactly 3 requests per 10 seconds per IP address. Exceeding this should return a `429 Too Many Requests` status.

3. **CI Test Script**:
   Create a test script at `/home/user/ci_test.sh` that a CI/CD pipeline can use to verify the mock server. It should start your server in the background, wait for it to be ready, and use `curl` to assert that:
   - A valid authenticated request returns the correct calculation and a 200 status code.
   - An invalid request returns 400.
   - Missing/bad auth returns 401.
   - Sending 4 rapid requests successfully triggers the 429 rate limit on the 4th request.
   Make sure the script exits with `0` on success and `1` on failure.

Run the server in the background (or leave it running in a tmux session) so our automated test suite can verify it against the required protocol.