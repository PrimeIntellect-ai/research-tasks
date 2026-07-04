You are a container specialist managing a microservices stack for a log ingestion pipeline. The system consists of three cooperating services running locally under `/home/user/app/`:
1. Nginx (Reverse Proxy & TLS termination)
2. A Python Flask application (Log Ingestion API)
3. Redis (Cache and Rate Limiting)

Currently, the stack is broken and vulnerable. Your objective is to fix the service communication, configure TLS, and implement an adversarial payload filter.

**Part 1: Service Gluing & Health Monitoring**
The startup script `/home/user/app/start.sh` launches all three processes in the background, but they are not communicating correctly.
- Nginx is supposed to listen on HTTPS port 8443 (localhost) and proxy requests to the Flask app on port 5000. Generate a self-signed certificate at `/home/user/app/certs/server.crt` and `/home/user/app/certs/server.key` and configure Nginx (`/home/user/app/nginx.conf`) to use them.
- The Flask app (`/home/user/app/app.py`) attempts to connect to Redis for rate-limiting, but it's using the wrong port. Configure it to connect to Redis on port 6379.
- Implement a `/health` endpoint in the Flask app that returns HTTP 200 `{"status": "ok", "redis": "connected"}` only if it can successfully ping Redis.

**Part 2: Adversarial Payload Filter**
The log ingestion endpoint `/ingest` receives JSON payloads. We have observed malicious payloads attempting to exploit storage quotas and inject path traversal attacks.
You must write a standalone Python module at `/home/user/validator.py` containing a function with the following signature:
`def validate_payload(filepath: str) -> bool:`

This function must read a JSON file and return `True` if the payload is safe, and `False` if it is malicious.
A payload is considered **malicious** (return `False`) if:
1. It contains any key or value with the substring `../` or `..\\`.
2. The "log_data" field is a string that exceeds 1024 characters (storage bloat attempt).
3. The JSON structure is invalid or cannot be parsed.

You are provided with two directories of test payloads to evaluate your script:
- `/home/user/corpus/clean/` (Valid, safe payloads)
- `/home/user/corpus/evil/` (Malicious payloads)

Once your `validator.py` is written, modify `/home/user/app/app.py` to import `validator_payload` and use it to validate the incoming POST request body (saving it to a temporary file first if necessary). If `False`, the endpoint must return HTTP 400.

**Part 3: Automation & CI**
Write a validation script at `/home/user/test_stack.sh` that:
1. Performs a `curl -k` to `https://127.0.0.1:8443/health` and saves the output to `/home/user/health_result.json`.
2. Loops through all files in `/home/user/corpus/clean/` and `/home/user/corpus/evil/`, POSTing them to `https://127.0.0.1:8443/ingest` using `curl -k`, and writes the HTTP status codes to `/home/user/ingest_results.txt` (format: `filename: status_code`).

Leave the services running and ensure `/home/user/test_stack.sh` executes successfully.