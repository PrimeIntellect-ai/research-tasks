You are an incident responder tasked with investigating and remediating a recent security breach in a multi-service authentication environment. Intelligence suggests the attackers exploited a vulnerability in how the authentication service handles JSON Web Tokens (JWTs) and took advantage of missing service isolation.

The environment is located in `/app/` and consists of three components started via `/app/start.sh`:
1. **Nginx** (Reverse Proxy) - Currently misconfigured or partially configured.
2. **Flask Auth API** (`/app/auth_service/app.py`) - Runs on port 5000.
3. **Redis** - Local cache running on port 6379.

Your objectives are divided into two phases: Remediation and Investigation.

### Phase 1: Remediation (Configuration & Patching)
1. **Process/Network Isolation**: The Flask app is currently bound to `0.0.0.0:5000`, exposing it directly to the network. Modify the application so it only binds to localhost (`127.0.0.1`), ensuring all external traffic must go through Nginx.
2. **TLS/SSL Certificate Management**: Configure Nginx (using its config file at `/app/nginx/nginx.conf`) to terminate TLS on port 443. The certificates are already generated and located at `/app/certs/server.crt` and `/app/certs/server.key`. Ensure Nginx proxies requests securely to the Flask backend. 
3. **Secure Coding (JWT Patch)**: The Flask application relies on PyJWT but fails to restrict the accepted signing algorithms, making it vulnerable to `alg: none` attacks. Modify `/app/auth_service/app.py` to explicitly enforce the `HS256` algorithm and safely validate the signature using the existing `SECRET_KEY`.

### Phase 2: Algorithmic Investigation
The service logs its authentication attempts (including the raw JWTs) to `/app/logs/auth.log`. Each line contains a JSON object with `timestamp`, `ip`, and `token`. 

Write a Python script at `/home/user/audit.py` that parses `/app/logs/auth.log`. Your script must algorithmicly identify all tokens that successfully exploited the `alg: none` vulnerability (tokens forged without a signature that the system previously accepted). 

For every compromised token, extract the `user_id` from the JWT payload. Have your script output a CSV file at `/home/user/compromised_users.csv` with exactly two columns: `user_id` and `timestamp`.

Ensure `/app/start.sh` runs successfully with your new configurations. Your environment fixes and your CSV output will be rigorously tested.