You are a DevSecOps engineer responsible for enforcing policy as code to secure an internal microservice architecture. A recent security audit found that the current API gateway allows JWTs with insecure algorithms (like `alg=none`) and lacks robust payload integrity checks. 

Your objective is twofold:
1. Develop a standalone Python validation script that strictly enforces token security, matching the exact behavior of our internal reference oracle.
2. Integrate this validator into a multi-service gateway pipeline (Nginx + Python Auth Service + Backend Service).

### Part 1: Token Validator (Fuzz Equivalence)
Write a Python script at `/home/user/verify_token.py`. The script must read a single raw JWT string from `stdin` and print exactly one of the following output strings to `stdout`, matching the exact logic of our compiled reference oracle (`/app/oracle/token_validator_bin`):

1. `MALFORMED`: If the input is not a valid 3-part base64url-encoded JWT.
2. `REJECTED_ALG`: If the JWT header specifies any algorithm other than exactly `RS256` (e.g., `none`, `HS256`, or missing).
3. `INVALID_SIG`: If the RS256 signature is invalid when verified against the public key located at `/app/certs/public.pem`.
4. `INTEGRITY_FAIL`: If the signature is valid, but the JWT payload does not contain a `file_hash` claim, OR the `file_hash` claim does not exactly match the SHA-256 hex digest of the local file `/app/data/critical_config.json`.
5. `VALID`: If all the above checks pass successfully.

Note: Do not print any extraneous text or logs to standard output. The automated tester will randomly fuzz your script against the oracle with thousands of malformed, maliciously crafted (e.g., signature stripped, `alg=none`), and valid tokens to assert bit-exact equivalence.

### Part 2: Gateway Integration
We have the following services that need to be glued together:
- **Backend Application**: An existing Python service running on `127.0.0.1:9000`.
- **Nginx Reverse Proxy**: An Nginx instance running with its config at `/home/user/nginx.conf`.
- **Auth Interceptor**: A Python HTTP server you must create at `/home/user/auth_service.py` to bind to `127.0.0.1:8081`.

You must configure the multi-service flow as follows:
1. Create `/home/user/auth_service.py`. It should be a lightweight HTTP server listening on `127.0.0.1:8081`. It must extract the token from the `Authorization: Bearer <token>` header, pass it to your `/home/user/verify_token.py` script via `stdin`, and return an HTTP `200 OK` if the script outputs `VALID`. For any other output (or missing header), it must return an HTTP `401 Unauthorized`.
2. Configure Nginx (`/home/user/nginx.conf`) to listen on `127.0.0.1:8080`.
3. Set up Nginx to use the `auth_request` module. All requests to Nginx (`/`) should trigger an `auth_request` to your Auth Interceptor (`127.0.0.1:8081`). 
4. If the auth request succeeds (200), Nginx must proxy the original request to the Backend Application (`127.0.0.1:9000`). If it fails (401), Nginx should return the 401 directly to the client.

Ensure your Python scripts use standard libraries or pre-installed packages (like `PyJWT` and `cryptography` which are available in the environment). 
When finished, leave the Nginx service and your `auth_service.py` running in the background. Create a file `/home/user/integration_done.log` containing the word `READY` when your entire setup is complete.