You are tasked with fixing a custom web backend and its Nginx reverse proxy configuration. Currently, requests to the Nginx proxy return a "502 Bad Gateway" error because the proxy is misconfigured, the directory structure is broken, and the C++ backend lacks a proper health check endpoint. 

Follow these instructions to resolve the system:

1. **Backup and Directory Setup:**
   - The primary Nginx configuration file is located at `/home/user/app/conf/nginx.conf`.
   - Before making any changes, back up this file to `/home/user/backup/nginx.conf.bak`. (You must create the `backup` directory first).
   - Create a logs directory at `/home/user/app/logs`.
   - Create a symbolic link at `/home/user/active_conf` pointing to the live configuration file (`/home/user/app/conf/nginx.conf`).

2. **C++ Backend Fix (`/home/user/app/src/server.cpp`):**
   - We have a simple custom C++ HTTP server listening on port `8081`.
   - Currently, it crashes or returns 404 for health checks. You must modify `/home/user/app/src/server.cpp` so that if an incoming HTTP GET request is for the `/health` path, it responds exactly with `HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK`.
   - Compile the server using `g++ /home/user/app/src/server.cpp -o /home/user/app/backend`.
   - Start the backend process in the background.

3. **Nginx Configuration Fix:**
   - Modify `/home/user/app/conf/nginx.conf`.
   - Fix the upstream block so it points to the correct backend Nginx port (the Nginx config currently routes traffic to port `9999`, but the C++ backend listens on `8081`).
   - Ensure Nginx writes its `pid` to `/home/user/app/nginx.pid` and `error_log` to `/home/user/app/logs/error.log` (these should already be in the Nginx config, just ensure the paths are correct).

4. **Start and Verify:**
   - Start Nginx in the background as the current user using: `nginx -c /home/user/app/conf/nginx.conf`
   - Wait 1-2 seconds for the services to start.
   - Run a `curl` request to Nginx Nginx (listening on `127.0.0.1:8080`) at the `/health` endpoint.
   - Save the raw output of this `curl` command to `/home/user/resolution.log`.