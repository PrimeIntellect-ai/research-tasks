You are a security auditor tasked with securing a microservices architecture. The system currently consists of three services running locally:
1. **API Gateway (Nginx)**: Runs on port 8080.
2. **Auth Service**: Runs on port 8081.
3. **Data Service**: Runs on port 8082.

Your task has two parts: Multi-service Configuration and Security Filter Implementation.

### Part 1: Service Configuration
The Nginx configuration at `/etc/nginx/nginx.conf` is currently incomplete. You must modify it so that:
- Requests to `http://127.0.0.1:8080/auth/...` are proxied to the Auth Service (`http://127.0.0.1:8081/...`).
- Requests to `http://127.0.0.1:8080/data/...` are proxied to the Data Service (`http://127.0.0.1:8082/...`).
Ensure Nginx is reloaded or restarted after your changes so the end-to-end flow is functional.

### Part 2: Security Filter Implementation (Go)
We need a standalone security auditing tool that processes backend logs. Write a Go program at `/app/auditor.go` and compile it to `/app/auditor`. 

The program must read exactly one line of JSON from standard input (`stdin`), process it, and print exactly one line of JSON to standard output (`stdout`).

**Input Format:**
`{"auth_header": "Bearer <jwt_token>", "response_body": "<string_content>"}`

**Security Rules:**
1. **CWE-287 / JWT Signature Bypass Auditing:** 
   Extract the JWT from the `auth_header`. A JWT has three parts separated by dots (`header.payload.signature`). Base64Url-decode the `header` part (it may lack padding). Parse the decoded header as JSON.
   - If the `alg` field is exactly `"none"`, `"NONE"`, or `""` (empty string), the tool must block the request.
   - **Block Output Format:** `{"action": "DROP", "reason": "CWE-287", "body": ""}`

2. **Sensitive Data Redaction (Pattern Matching):**
   If the JWT is valid (i.e., `alg` is present and not none-equivalent), you must sanitize the `response_body` for Data Loss Prevention (DLP):
   - **SSNs:** Find any sequence matching `DDD-DD-DDDD` (where D is a digit 0-9) and replace the entire matched sequence exactly with `[REDACTED-SSN]`.
   - **Credit Cards:** Find any sequence matching `DDDD-DDDD-DDDD-DDDD` and replace the entire matched sequence exactly with `[REDACTED-CC]`.
   - **Allow Output Format:** `{"action": "ALLOW", "reason": "", "body": "<sanitized_string_content>"}`

**Requirements:**
- The compiled executable must be located at `/app/auditor`.
- It must handle potentially malformed JWTs gracefully (if it cannot parse the JWT header, treat it as `DROP` with reason `MALFORMED`).
- Do not output any extraneous text or logs to stdout. Stdout must strictly contain the JSON result.