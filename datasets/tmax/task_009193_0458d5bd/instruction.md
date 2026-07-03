You are tasked with fixing a malfunctioning local web stack running in user-space. The system consists of an Nginx reverse proxy and a Python backend service managed by a custom process monitor. Currently, accessing the proxy returns a 502 Bad Gateway error.

Your objectives:
1. Nginx is configured at `/home/user/app/nginx.conf` to listen on port 8080. It currently expects the backend to be at `127.0.0.1:9090`.
2. The Python backend script `/home/user/app/backend.py` and its process monitor `/home/user/app/monitor.py` are misconfigured. The backend is either failing to start or listening on the wrong network interface/port.
3. Diagnose the issue and modify the configuration files (`nginx.conf`) and/or Python scripts (`monitor.py`, `backend.py`) so that the Nginx proxy successfully routes requests to the backend.
4. When correctly configured, making a GET request to `http://127.0.0.1:8080` must return an HTTP 200 OK with the exact body text: `Backend Active`
5. Ensure both the Nginx process (using the provided config) and the Python monitor script are running in the background. Nginx must be started using: `nginx -c /home/user/app/nginx.conf -g 'pid /home/user/app/nginx.pid; daemon on;'` (or similar user-space execution).
6. Once the system is stable, write a Python script at `/home/user/app/test_stack.py` that performs an HTTP GET request to `http://127.0.0.1:8080`. The script must append the result to a log file at `/home/user/app/success.log` in the exact format: `STATUS: <status_code>, BODY: <response_text>`.
7. Execute `/home/user/app/test_stack.py` at least once to generate the log file.

Note: You do not have root access. All services must run as the default user. Do not use privileged ports (under 1024). Nginx must write its error and access logs to `/home/user/app/` (which is already set up in the initial `nginx.conf`).