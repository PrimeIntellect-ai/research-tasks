As a FinOps analyst, I need you to implement an automated cost-control routing system for our hybrid cloud storage. We want to route incoming file-processing requests away from expensive storage tiers when their usage quota is exceeded. 

Since you do not have root access, everything must be run locally in `/home/user/`. Nginx and a C compiler (`gcc`) are already installed.

Please implement the following pipeline:

**Phase 1: Storage Monitoring Script**
1. I have placed a mock mount configuration file at `/home/user/cost_fstab`. Its format mimics `/etc/fstab`, but it contains custom mount options like `tier=expensive` or `tier=cheap`.
2. Write a bash shell script at `/home/user/monitor_storage.sh`.
3. The script must parse `/home/user/cost_fstab`, find all directory paths configured with the `tier=expensive` option, and calculate their combined total disk usage in bytes using `du -sb`.
4. The script must write only the total combined integer byte count to `/home/user/expensive_usage.txt` (overwriting the file each time).

**Phase 2: Quota Enforcement Server (C)**
1. Write a C program at `/home/user/quota_server.c` and compile it to `/home/user/quota_server`.
2. The server must be a basic HTTP server listening on `127.0.0.1` port `9000`.
3. For every incoming HTTP GET request, it should open and read the integer from `/home/user/expensive_usage.txt`.
4. If the value is strictly greater than `102400` (100 KB), the server must respond with an `HTTP/1.1 503 Service Unavailable` status and the body `Quota Exceeded`.
5. If the value is less than or equal to `102400`, the server must respond with an `HTTP/1.1 200 OK` status and the body `Traffic Allowed`.
6. Run this server in the background.

**Phase 3: Cost-Aware Reverse Proxy**
1. Create an Nginx configuration file at `/home/user/nginx.conf`.
2. Configure Nginx to listen on `127.0.0.1:8080` and act as a reverse proxy to your C server on port `9000`.
3. Configure Nginx to run entirely as a non-root user (you must set directives like `pid`, `error_log`, `access_log`, `client_body_temp_path`, `proxy_temp_path`, etc., to point to writable directories inside `/home/user/nginx_run/`).
4. If the upstream C server returns a `503` error, Nginx must intercept this error (`proxy_intercept_errors on;`) and internally redirect to serve a static fallback file located at `/home/user/fallback.html`.
5. Create `/home/user/fallback.html` containing exactly the text: `Routed to cheap storage`.
6. Start Nginx in the background using your custom configuration.

Ensure all services (the C server and Nginx) are running concurrently when you complete your task.