You are a security engineer tasked with rotating credentials and replacing a vulnerable legacy authentication component in our system. 

Our application architecture under `/app/` consists of three services:
1. An Nginx reverse proxy.
2. A backend API (Flask).
3. A legacy token validation service (`/app/bin/legacy_auth`, a compiled ELF binary).

Recently, we discovered that `legacy_auth` is vulnerable: it improperly validates JSON Web Tokens (JWTs) when the algorithm is set to `none`, bypassing signature checks. We need to replace this binary with a secure Python implementation and reconfigure the system.

Your objectives are:

1. **Analyze the Legacy Binary:** Inspect `/app/bin/legacy_auth` to understand its expected input and output formats. It takes a JWT as a command-line argument, validates it (using a hardcoded secret key hidden in the binary), and outputs a specific JSON response. 

2. **Write a Secure Python Replacement:** Create a Python script at `/home/user/secure_auth.py`. 
    - It must accept a single command-line argument (the JWT).
    - It must reproduce the EXACT SAME output behavior as `legacy_auth` for all properly signed tokens.
    - It MUST reject any token where the algorithm is `none` (or missing) by exiting with code `1` and printing `{"status": "error", "reason": "invalid_algorithm"}`.
    - Extract the hardcoded secret key from the legacy ELF binary to use in your Python implementation.

3. **Multi-Service Composition & Process Isolation:** 
    - The services are defined in `/app/docker-compose.yml` (simulated for this environment using local startup scripts at `/app/start_services.sh`).
    - Nginx is configured to forward requests to the auth service. Update the Nginx configuration at `/app/nginx/nginx.conf` so that token validation requests are routed to a new local endpoint handled by your Python script.
    - Update the startup script (`/app/start_services.sh`) to launch your Python script as a persistent service listening on port 8081.
    - To enforce process isolation, your Python service must be run using `bwrap` (Bubblewrap) restricting read access only to `/home/user/` and `/usr/`, and with no network access other than binding to port 8081.

4. **Intrusion Detection Pattern Matching:**
    - Add a pattern-matching rule to Nginx (via `map` or standard regex in `nginx.conf`) to immediately drop any incoming HTTP requests where the `Authorization` header contains the string `"alg":"none"` (base64 encoded variants), returning a 403 Forbidden.

Ensure all services start correctly when `/app/start_services.sh` is executed. The verifier will test your `secure_auth.py` script rigorously against the legacy binary.