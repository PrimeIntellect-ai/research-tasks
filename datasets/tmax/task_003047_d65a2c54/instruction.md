You are a Cloud Architect migrating an old C++ microservice to a new local reverse-proxy setup using Nginx. 

Currently, the stack is broken. Nginx is returning a 502 Bad Gateway when accessing the API, and several components are missing or misconfigured. 

Your objective is to fix the C++ service, configure Nginx correctly as a reverse proxy, set up local port forwarding, and ensure the service interacts correctly with the filesystem.

Here are your specific tasks:

1. **Fix the C++ Microservice**:
   - The source code is located at `/home/user/service/main.cpp`.
   - The service is supposed to listen on a Unix Domain Socket (UDS) at `/home/user/service/backend.sock`. However, there is a bug in the code causing it to bind to the wrong path. Find and fix this bug.
   - When the service receives an HTTP GET request to `/api/migrate`, it must read the contents of `/home/user/data/migration_target.txt`.
   - It must then write the exact string `MIGRATION_COMPLETE_TO_<target>` (where `<target>` is the exact string read from the file) to `/home/user/data/migration_status.txt`.
   - Fix the socket path, compile the service (output to `/home/user/service/backend_service`), and start it in the background.

2. **Configure Nginx**:
   - The Nginx configuration file is located at `/home/user/nginx/nginx.conf`.
   - Update it to run completely in user space (do not use port 80 or root privileges).
   - Configure it to listen on port `8080`.
   - Set up a location block for `/api/` that proxies requests to the C++ service's Unix Domain Socket at `/home/user/service/backend.sock`.
   - Implement basic access control in the Nginx config: only allow traffic from `127.0.0.1` and deny all other IP addresses.
   - Start Nginx using this configuration file (e.g., `nginx -c /home/user/nginx/nginx.conf`).

3. **Configure Port Forwarding**:
   - Due to legacy system requirements, the external client will attempt to connect to port `9090`.
   - Use `socat` to forward TCP port `9090` to the Nginx listening port `8080`. Run this in the background.

4. **Trigger and Verify**:
   - Make a `curl` request to `http://127.0.0.1:9090/api/migrate`.
   - Save the HTTP response body to `/home/user/test_result.txt`.

Ensure all background processes (the C++ service, Nginx, and socat) remain running.