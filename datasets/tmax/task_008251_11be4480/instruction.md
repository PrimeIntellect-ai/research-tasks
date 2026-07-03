You are an application security engineer and penetration tester. We have discovered a potential vulnerability in an internal C++ daemon used for SSH key management. This daemon listens for HTTP requests, extracts a JWT from the `Authorization: Bearer <token>` header, and if the user has the `"admin"` role, adds an SSH key from the payload into a managed `authorized_keys` file.

The source code for the service is located at `/home/user/jwt_service/server.cpp`. It has a custom, naive JWT parser.

Your tasks are:
1. **Vulnerability Analysis & Exploitation:** Analyze `/home/user/jwt_service/server.cpp`. Identify the vulnerability that allows bypassing signature validation (hint: algorithm manipulation). Exploit the locally running server (on port 8080) to inject the following SSH key into `/home/user/jwt_service/managed_authorized_keys`:
   `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPfakekeyhere admin@hack`
   Save the exact forged JWT string you used to `/home/user/exploit_token.txt`.

2. **Secure Coding (C++):** Fix the vulnerability in `/home/user/jwt_service/server.cpp`. Specifically, ensure that the server rejects any JWT where the `alg` field in the header is `"none"` (case-insensitive) or empty. If an invalid or unauthenticated token is provided, the server must respond with HTTP status `401 Unauthorized`.
   Recompile the server using the provided `/home/user/jwt_service/Makefile`. The resulting binary should be at `/home/user/jwt_service/server`.

3. **Automated Vulnerability Scanning:** Write a bash script at `/home/user/vuln_scanner.sh` that acts as an automated vulnerability scanner for this specific issue. 
   - It should take a target as its first argument (e.g., `localhost:8080`).
   - It should construct an HTTP POST request with a crafted `alg=none` JWT containing an arbitrary SSH key.
   - It should inspect the HTTP response headers/status.
   - It should print exactly `VULNERABLE` to stdout if the server accepts the payload (e.g., returns 200 OK), or `SECURE` if the server rejects it with a 401.
   - Make the script executable.

Ensure the patched server is running on port 8080 before completing your task, as it will be tested by our automated suite.