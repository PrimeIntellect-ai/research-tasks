You are an incident responder tasked with investigating a recent breach on a web application. The application stack consists of Nginx, a Flask API, and a Redis backend. The attacker managed to bypass authentication by exploiting a JWT verification flaw (specifically, the application accepted tokens with `algorithm="none"`).

Your objective is to restore the services securely, analyze the logs to identify the attacker, and write a robust JWT verification filter.

**Phase 1: Multi-Service Restoration**
The application stack is located in `/app/`. You can start the services by running `/app/start_services.sh`. Currently, the system is broken:
1. **TLS Misconfiguration:** The Nginx reverse proxy (listening on port 8443) is failing to start because it is missing its SSL certificates. Generate a self-signed certificate and key at `/app/nginx/ssl/cert.pem` and `/app/nginx/ssl/key.pem`. 
2. **Proxy Routing:** Nginx is configured to proxy requests to the Flask API, but the configuration at `/app/nginx/nginx.conf` has the wrong backend port. Audit the Flask service (which starts via the script) to find the correct port, and fix the Nginx configuration so that requests to `https://127.0.0.1:8443/api/health` return a successful 200 OK response from Flask. (Use `-k` with curl to ignore self-signed cert warnings).

**Phase 2: Log Analysis**
The attacker left traces in `/app/logs/api_access.log`. The logs contain the base64-encoded JWTs submitted in the `Authorization: Bearer <token>` header, along with the source IP addresses.
1. Parse this log file.
2. Decode the JWT headers to find the token that uses `{"alg": "none"}` (or `none` in any casing).
3. Extract the IP address of the attacker who submitted this token and write it exactly to `/home/user/attacker_ip.txt`.

**Phase 3: Adversarial JWT Filter**
To prevent this in the future, we need a standalone Python classifier to sanitize incoming tokens. The Flask app uses the HMAC secret: `Secret-Responder-Key-99!`.
Write a script at `/home/user/jwt_filter.py`. Your script will be tested against two sets of tokens provided by our automated pipeline.
*   **Invocation:** `python3 /home/user/jwt_filter.py <input_directory> <output.json>`
*   **Logic:** For each file in `<input_directory>` (which contains one raw JWT string per file), validate the token using the secret above. The token must be valid, not expired, have a valid signature, and strictly use the `HS256` algorithm. It MUST reject `none` algorithms or algorithm confusion attempts.
*   **Output:** Write a JSON dictionary to `<output.json>` mapping the filename to a boolean: `true` if the token is completely valid and secure, and `false` if it is invalid, expired, or malicious.

Ensure your script handles exceptions gracefully and correctly classifies every file in the given directory.