You are acting as a penetration tester auditing a local web application. 

A locally developed application is located in `/home/user/vuln_app/`. The developers have implemented a custom JWT (JSON Web Token) authentication mechanism. We suspect it is vulnerable to the "Algorithm None" (`alg=none`) signature bypass vulnerability.

Your task is to exploit this vulnerability to retrieve a secret flag. Follow these steps precisely:

1. **Log Parsing:** The application maintains an authentication log at `/home/user/vuln_app/auth.log`. Parse this log to identify the exact username of the administrator. You will need to find a log entry that explicitly mentions a user with `role=admin`.

2. **Process Isolation / Sandboxing:** The application is not running yet. Start the application by executing `/usr/bin/python3 /home/user/vuln_app/server.py &`. It will bind to `127.0.0.1:8080`.

3. **Exploitation:** 
   - Construct a forged JWT to impersonate the administrator you identified in step 1.
   - The token must use the `none` algorithm bypass (e.g., `{"alg": "none", "typ": "JWT"}`).
   - The payload must contain the administrator's username in the `username` claim (e.g., `{"username": "<admin_username>"}`).
   - Send an HTTP GET request to `http://127.0.0.1:8080/api/flag` with your forged token in the `Authorization: Bearer <token>` header.

4. **Checksum Verification:** 
   - If successful, the server will respond with a JSON object containing a `flag` key.
   - Extract the flag string from the JSON response.
   - Compute the SHA-256 cryptographic hash (hex digest) of the exact flag string (no trailing newlines).
   - Write ONLY the SHA-256 hex digest to `/home/user/solution.txt`.

Note: Standard base64url encoding must be used for the JWT header and payload. The token must have three parts separated by dots, with the signature part being empty.