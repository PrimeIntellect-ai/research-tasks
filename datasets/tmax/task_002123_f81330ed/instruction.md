You are tasked with diagnosing a failing systemd user service, fixing the underlying application, and setting up a load-balanced reverse proxy with log rotation.

We have a vendored Python web service located at `/app/vendor/simple_service`. It is meant to be run as a user-level systemd service, but it currently fails to start. 

Here are your objectives:
1. **Fix the Service**: Diagnose and fix the Python code in `/app/vendor/simple_service/server.py`. The application is supposed to take a port number as its first command-line argument and listen on `127.0.0.1` on that port. It should return an HTTP 200 response with the text `Served by <port>`.
2. **Run Backends**: Start three instances of this service listening on ports `8001`, `8002`, and `8003`. Since you don't have root access, run them as background processes or user systemd services.
3. **Configure Load Balancer**: Write an idempotent Python script at `/home/user/setup_balancer.py` that generates an Nginx configuration file at `/home/user/nginx/nginx.conf`. The Nginx server must listen on `127.0.0.1:8080` and load-balance incoming HTTP requests across the three backend instances using a strict round-robin algorithm. Nginx should write its access logs to `/home/user/nginx/access.log` and store its pid file in `/home/user/nginx/nginx.pid`.
4. **Start Proxy**: Create a script `/home/user/start_nginx.sh` that starts Nginx as the current user using the generated configuration.
5. **Log Rotation**: Write a Python script at `/home/user/rotate_logs.py` that renames `/home/user/nginx/access.log` to `/home/user/nginx/access.log.1` and signals Nginx (via its PID file) to reopen its log files, mimicking standard log rotation behavior.

Ensure that the backend distribution is perfectly balanced. An automated verifier will send 300 requests to the load balancer and check if the traffic is evenly distributed across the 3 backend ports.