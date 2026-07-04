As a FinOps analyst, you are implementing a "scale-to-zero" cost optimization strategy for our internal analytics service. The heavy analytics service consumes resources even when idle, so we want to put it behind a wake-on-request reverse proxy.

Your task is to build this system entirely in user space (no root access required) using Python and process supervision.

Step 1: Environment Setup
Add an environment variable `FINOPS_PROXY_PORT=8080` to `/home/user/.bashrc`.

Step 2: The Wake-on-Request Proxy
Write a Python script at `/home/user/scale_to_zero_proxy.py` that does the following:
- Retrieves the listening port from the `FINOPS_PROXY_PORT` environment variable.
- Starts an HTTP server on `127.0.0.1` at that port.
- When an HTTP GET request is received:
  1. Checks if the backend analytics service is responding on `127.0.0.1:9090`.
  2. If it is not responding, spawns the service by running `python3 /home/user/analytics_service.py` as a detached background process, and waits for it to become available (poll port 9090 until it responds).
  3. Acts as a reverse proxy by forwarding the GET request to `http://127.0.0.1:9090` and returning the exact backend response and status code to the original client.

Step 3: Process Supervision
We need to ensure your proxy script runs continuously. Create a supervisord configuration file at `/home/user/supervisor.conf`. 
Configure it to manage a program named `finops_proxy` that runs `/usr/bin/env python3 /home/user/scale_to_zero_proxy.py`. Set `autorestart=true` and ensure it runs in the foreground of the supervisor (`nodaemon=false` in the `[supervisord]` section, or leave default). Include standard `[supervisord]` and `[supervisorctl]` blocks suitable for a non-root user (put logs and pid files in `/home/user/`).

Constraints:
- Only use standard library modules in your Python proxy (e.g., `http.server`, `urllib.request`, `subprocess`, `socket`, `time`, `os`).
- Do not modify `/home/user/analytics_service.py` (assume it already exists).
- Do not start the supervisor yourself; the automated verification will start `supervisord -c /home/user/supervisor.conf` and issue test requests.