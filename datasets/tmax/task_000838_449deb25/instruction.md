You are a Site Reliability Engineer monitoring uptime for our microservices platform. We have an incoming webhook ingestion pipeline for uptime metrics, composed of three services:
1. An Nginx reverse proxy
2. A Python Flask application that acts as the webhook receiver
3. A Redis backend

Currently, the system is completely broken. The services are not properly connected, and the payload validation script is crashing on edge cases. 

Your tasks are:

**1. Service Composition & Reconfiguration**
The startup script brings up Nginx, Flask (via Gunicorn), and Redis. However, the end-to-end flow is broken.
- Reconfigure Nginx (`/app/nginx/nginx.conf`) to proxy requests to the `/intake` endpoint to the Flask app running on `127.0.0.1:5000`. Nginx runs on port 8080.
- Reconfigure the Flask app's environment variables (located in `/app/flask/.env`) so that it connects to Redis on `127.0.0.1:6379` instead of a hardcoded remote host.

**2. Fix the Sanitizer (Debugging)**
The Flask app relies on a middleware script `/app/flask/sanitizer.py` to validate incoming JSON payloads. This script has several critical bugs:
- **Loop termination / Recursion:** Payloads contain a `component_tree` dictionary defining dependency relationships (e.g., `{"A": ["B"], "B": ["C"]}`). The `check_cycles()` function uses recursion but lacks cycle detection, causing a RecursionError (stack overflow) when malicious actors send cyclical dependencies (e.g., `{"A": ["B"], "B": ["A"]}`). Fix it so it returns `False` (REJECT) on cycles.
- **Precision loss tracking:** Payloads contain `start_ns`, `end_ns`, and `duration_ns` as massive integer strings (nanosecond precision). The validator currently casts these to standard Python `float` for comparison, which causes precision loss. Malicious payloads exploit this by sending `duration_ns` values that are off by a few nanoseconds but pass the float comparison. Fix it to evaluate them using exact integer arithmetic, REJECTING if `end_ns - start_ns != duration_ns`.

**Goal & Output:**
Modify the configurations and `/app/flask/sanitizer.py` so that the end-to-end pipeline accepts valid metrics (saving them to Redis) and returns a 400 error for invalid metrics.
You must test your solution against the sample payloads provided in `/app/corpus/clean/` and `/app/corpus/evil/`. 

To finish the task, ensure the services can be cleanly started via `/app/start_all.sh` and routing works correctly.