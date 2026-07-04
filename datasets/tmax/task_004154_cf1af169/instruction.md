You are a network engineer tasked with troubleshooting and securing a misconfigured microservices stack. The system consists of multiple cooperating user-space services managed by a local startup script, but currently, they cannot communicate properly, and the application is exposed to malicious payloads.

Your objective is to fix the network routing between the services and implement a robust Web Application Firewall (WAF) reverse proxy in Python. 

**System Architecture (Desired State):**
1. **Nginx** (Reverse Proxy) - Listens on `127.0.0.1:8080`.
2. **Python WAF** (Security Filter) - Listens on `127.0.0.1:8081`.
3. **Python API** (Backend App) - Listens on `127.0.0.1:8082`.
4. **Redis** (Cache) - Listens on `127.0.0.1:6379`.

**The End-to-End Flow:**
External Client -> HTTP POST `/process` -> Nginx (`:8080`) -> WAF (`:8081`) -> API (`:8082`) -> Redis (`:6379`).

**Current Issues You Must Fix:**
1. **Network Misconfiguration:** The startup script `/home/user/app/start_services.sh` and the Nginx configuration `/home/user/app/nginx.conf` have incorrect port bindings and routing. Nginx is currently bypassing the WAF and proxying directly to a dead port. Fix `nginx.conf` and any bindings in `start_services.sh` / `api.py` so the exact chain above works.
2. **WAF Implementation:** You must write the Python WAF from scratch at `/home/user/app/waf.py`. 
    * It must be an HTTP server (using Flask, FastAPI, or standard library) listening on `8081`.
    * It must accept POST requests on `/process`.
    * It must inspect the JSON payload.
    * It must act as a reverse proxy: if the payload is safe, forward the exact request to the Backend API on `8082` and return the API's response to the client.
    * If the payload is malicious, it must immediately return an HTTP 403 Forbidden without forwarding to the backend.
3. **Adversarial Tuning:** We have provided two directories containing sample JSON payload files:
    * `/home/user/corpus/clean/`: Contains 50 normal requests.
    * `/home/user/corpus/evil/`: Contains 50 malicious requests.
    Analyze these files to determine the specific patterns, keywords, or anomalies that distinguish evil payloads from clean ones. Implement the detection logic in `waf.py` accordingly.
4. **Permissions:** Ensure that `/home/user/app/waf.py` has strictly `700` permissions (read/write/execute only by the user).

**Verification:**
Once you have fixed the configs and written `waf.py`, run `/home/user/app/start_services.sh` to bring up the stack. Our automated test will then fire HTTP POST requests to `http://127.0.0.1:8080/process`. You succeed if 100% of the clean payloads return HTTP 200 and 100% of the evil payloads return HTTP 403, and the service chain is correctly utilized.