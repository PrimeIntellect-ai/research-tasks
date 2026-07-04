You are a security engineer tasked with remediating a critical vulnerability, rotating compromised credentials, and enforcing a strict Content Security Policy (CSP) for an internal Python web service.

The application is located at `/home/user/app`. It consists of a Flask application in `/home/user/app/server.py` and a configuration file in `/home/user/app/config.json`.

Your objectives are:

1. **Vulnerability Remediation (JWT 'alg=none' bypass)**:
   The application uses a custom JWT verification function that is vulnerable to the 'alg=none' bypass attack. Modify `/home/user/app/server.py` so that it strictly rejects any token where the algorithm (`alg`) in the header is `'none'`, returning a `401 Unauthorized` instead. It must only accept signatures validated with the application's secret.

2. **Credential Rotation**:
   The current JWT secret has been exposed. Update `/home/user/app/config.json` to change the `JWT_SECRET` from its current value to exactly `"r0tated_s3cr3t_999"`. Make sure the application reads this new secret.

3. **Content Security Policy Enforcement**:
   The `/api/data` endpoint lacks proper security headers. Modify `server.py` to ensure that successful (200 OK) responses from `/api/data` include the following HTTP header exactly:
   `Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-random123';`

4. **Automated Vulnerability Scanning Script**:
   Write a Python script at `/home/user/app/scanner.py` that automated testing pipelines can run. When executed, this script must send two GET requests to `http://localhost:5000/api/data`:
   - Request A: A request with a mocked JWT token in the `Authorization: Bearer <token>` header that attempts an 'alg=none' bypass.
   - Request B: A request with a valid JWT token signed correctly using the new secret (`"r0tated_s3cr3t_999"`).

   The scanner must evaluate the responses and write its findings to a JSON file at `/home/user/app/scan_results.json` with exactly the following schema:
   ```json
   {
     "alg_none_rejected": true_or_false,
     "csp_enforced": true_or_false
   }
   ```
   - `alg_none_rejected` must be `true` if Request A receives a 401 status code.
   - `csp_enforced` must be `true` if Request B receives a 200 status code AND the response headers include the exact CSP header specified in step 3.

Ensure the Flask app runs successfully after your changes. You can test your `scanner.py` against the running server to verify your implementation.