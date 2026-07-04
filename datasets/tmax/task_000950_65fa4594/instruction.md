We are deploying a microservices architecture that has recently been flagged for potential JWT vulnerabilities, specifically related to signature bypass attacks (e.g., `alg=none`, key confusion) and anomalous access patterns. 

Your objective as a DevSecOps engineer is to implement a Python-based security middleware (WAF) and configure our service stack to route traffic securely.

The current system has the following components installed but not fully configured:
- Nginx (edge proxy)
- A Flask API service handling backend logic
- Redis for caching

You must accomplish the following:

1. **Write a WAF Service (`/home/user/waf/waf.py`):**
   Create a Python HTTP server (running on `127.0.0.1:8080`) that acts as a reverse proxy to the backend Flask API (`127.0.0.1:5000`). 
   The WAF must inspect all incoming HTTP requests for an `Authorization` header containing a Bearer JWT or a cookie named `session_token`.
   You must parse the JWT headers and payload (without relying on external libraries like `PyJWT` for the validation logic, you must decode the base64 manually to inspect the headers).
   The WAF must REJECT (return HTTP 403) any request where the JWT:
   - Has `alg` set to `none`, `None`, `NONE`, or an empty string.
   - Has a mismatched signature type (e.g., symmetric key used for asymmetric algorithm - detect if `alg` is `HS256` but the token corresponds to known public keys).
   - Fails a file integrity check: A log of valid issuer hashes is stored at `/home/user/data/valid_issuers.sha256`. Reject if the `iss` claim's SHA256 hash is not in this file.
   
   If the token is clean, forward the request to the Flask API and return its response. 
   
2. **Service Configuration:**
   - Configure Nginx (`/home/user/nginx/nginx.conf`) to listen on port 80 and forward all `/api/` requests to your WAF on port 8080.
   - Configure the Flask app (`/home/user/api/app.py`) to connect to Redis on `127.0.0.1:6379`.
   - Write a startup script `/home/user/start_services.sh` that starts Redis, Flask, your WAF, and Nginx.

3. **Security Logging:**
   Your WAF must log all rejected requests to `/home/user/logs/waf_blocks.log` in the format:
   `[TIMESTAMP] REJECTED: IP=<client_ip> REASON=<alg_none|invalid_issuer|key_confusion>`

You are provided with a test suite that will evaluate your WAF. The test suite will send hundreds of requests through Nginx on port 80. Your WAF must correctly reject all malicious tokens and allow all clean tokens.