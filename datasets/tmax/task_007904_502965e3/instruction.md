You are acting as a compliance security analyst. You have been tasked with generating an automated audit trail for a locally running microservice that is suspected of having multiple severe vulnerabilities. 

A local service is already running on `http://127.0.0.1:8080`.
The service exposes the following endpoints:
1. `GET /admin` - Requires a JWT token in the `Authorization: Bearer <token>` header. It is suspected to have a flawed JWT implementation that accepts tokens with the algorithm set to `none`.
2. `POST /search` - Accepts JSON data `{"query": "<search_term>"}`. It is suspected to be vulnerable to both SQL Injection and Cross-Site Scripting (XSS).

Your objective is to write a Bash script named `/home/user/generate_audit.sh` that acts as an automated vulnerability scanner and authentication flow tester. When executed, your script must:

1. **JWT Authentication Flow Testing:**
   Forge a JWT token to bypass authentication for the `/admin` endpoint. The token must claim the role of `admin` (i.e., payload `{"role": "admin"}`) and exploit the `alg: none` vulnerability. Send a request to `/admin` with this forged token. If successful, the endpoint will return a JSON response containing a `"secret_data"` field.

2. **Injection & XSS Vulnerability Analysis:**
   Send two separate requests to the `/search` endpoint:
   - Request A (SQLi): Send the exact payload `' OR 1=1 --` as the query.
   - Request B (XSS): Send the exact payload `<script>alert('audit')</script>` as the query.

3. **Audit Trail Generation:**
   Based on the responses, your script must generate a strict JSON log file at `/home/user/audit_report.json` containing the results of your audit. The JSON must have exactly the following structure:
   ```json
   {
     "jwt_bypass_successful": true,
     "admin_secret": "<the value of the secret_data field returned by /admin>",
     "sqli_response_code": <HTTP status code returned by Request A>,
     "xss_response_body": "<The exact raw text of the response body from Request B>"
   }
   ```

Requirements:
- Ensure your Bash script is executable.
- Do not use any external scanning tools like `sqlmap` or `nmap`; you must use standard bash utilities (e.g., `curl`, `jq`, `base64`, `sed`, `awk`).
- The generated `/home/user/audit_report.json` must be valid JSON.
- Run your script to ensure the `/home/user/audit_report.json` file is successfully created before completing the task.