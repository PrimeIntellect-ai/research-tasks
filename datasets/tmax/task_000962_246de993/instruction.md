You are a network engineer tasked with securing a multi-service web application that is actively being targeted by attackers. The application consists of three services located in `/home/user/app/`:
1. Nginx reverse proxy (intended to listen on port 8080).
2. Python Flask backend API (listens on port 5000).
3. Redis instance for token validation (listens on port 6379).

**Part 1: Service Composition**
The services are currently misconfigured and not communicating. 
- You must update `/home/user/app/nginx/nginx.conf` so that all requests to port 8080 are proxied to the Flask backend at `127.0.0.1:5000`.
- Update the Flask configuration in `/home/user/app/flask/config.py` to point to the local Redis instance (`127.0.0.1:6379`) instead of the dummy placeholder.
- Start all three services in the background.

**Part 2: Traffic Inspection & Log Parsing**
Once the services are running, a background traffic generator will send a mix of legitimate and malicious HTTP requests to the Nginx proxy (port 8080) for 30 seconds. The malicious requests attempt to exploit a known token validation vulnerability using specific crafted payloads (SQLi and command injection embedded in the `Authorization` header) and path traversal in the URI.

The Nginx access logs will be written to `/home/user/app/logs/access.log`.

**Part 3: IDS Filter Script**
Your primary objective is to write a Bash script located at `/home/user/ids_filter.sh`. 
This script must:
1. Accept the path to the Nginx access log as its first argument.
2. Use pattern matching and log parsing to identify the IP addresses of malicious actors. 
3. Output *only* the unique IP addresses that should be blocked, one per line, to standard output.

Malicious behavior is defined as:
- Any request containing `../` or `%2e%2e%2f` in the URI.
- Any request where the `Authorization` header (if logged) or URI query parameters contain SQL keywords like `UNION SELECT` or command injection patterns like `; rm` or `$(whoami)`.
- IPs that make more than 50 requests with invalid tokens (HTTP 401 response from the backend) within the log period.

**Evaluation:**
Your script `/home/user/ids_filter.sh` will be evaluated against a held-out access log containing 5,000 requests. We will compute the F1-score of the IPs your script identifies as malicious versus the ground truth. Your script must achieve an F1-score >= 0.95.

Ensure your Bash script is executable and robust. Do not rely on root access.