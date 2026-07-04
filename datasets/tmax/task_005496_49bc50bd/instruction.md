You are a network security engineer tasked with securing and testing an internal Go-based file upload service. The service is currently vulnerable to path traversal attacks and lacks proper authentication. 

Your objective is to implement security middleware in Go, fix the vulnerabilities, and write a comprehensive test suite to verify the security controls.

Here is the setup:
The source code is located at `/home/user/workspace/`. You will need to initialize the Go module (`go mod init uploadservice` and fetch necessary dependencies like `github.com/golang-jwt/jwt/v5`).

1. **Token Validation (Authentication):**
   Create a middleware function in a new file `/home/user/workspace/middleware.go` that inspects incoming HTTP requests for a cookie named `session_token`. 
   - Parse and validate this cookie as a JWT (JSON Web Token) using the HMAC-SHA256 algorithm.
   - The shared secret for the JWT is `network-sec-secret-2024`.
   - If the token is missing, invalid, or expired, return an HTTP 401 Unauthorized response.

2. **Pattern Matching & Inspection (IDS):**
   Extend the middleware to inspect the HTTP header `X-File-Name`.
   - Implement pattern matching to detect path traversal attempts. You must flag any filename containing `../`, `..\`, or starting with `/`.
   - If a traversal attempt is detected, append an alert line exactly matching: `[ALERT] Path traversal attempt blocked for filename: <filename>` to the log file `/home/user/workspace/ids_alerts.log`. 
   - Return an HTTP 403 Forbidden response for these malicious requests.

3. **Secure the Upload Handler:**
   Write the main server code in `/home/user/workspace/server.go` with a single endpoint `/upload` (POST) wrapped by your middleware. If the request passes the middleware, it should respond with HTTP 200 OK and the body `Upload successful`. (You do not need to implement actual file saving for this task, just the handler and middleware).

4. **Testing Suite:**
   Write a Go test file `/home/user/workspace/server_test.go` to test your implementation. The test suite must use `net/http/httptest` to simulate requests to your handler.
   It must include the following test cases:
   - A request with a valid JWT and a safe `X-File-Name` (e.g., `report.pdf`) -> Expect 200 OK.
   - A request missing the `session_token` cookie -> Expect 401 Unauthorized.
   - A request with a valid JWT but a malicious `X-File-Name` (e.g., `../../../etc/passwd`) -> Expect 403 Forbidden.

Once your code is complete and the tests pass, run your tests using `go test -v > /home/user/workspace/test_results.log`.

Make sure `/home/user/workspace/ids_alerts.log` is created during the test run when the malicious request is blocked.