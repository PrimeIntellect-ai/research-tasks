We are trying to deploy a high-performance custom C backend behind an Nginx reverse proxy, but we are currently getting "502 Bad Gateway" errors and terrible throughput. We need your help to fix the application, the proxy configuration, and the deployment script.

Here is what you need to do:

1. **Network Topology (Image Fixture):**
   Examine the architecture diagram located at `/app/architecture.png`. It contains the intended port assignments for the Nginx proxy and the two upstream backend instances. You must use these exact ports.

2. **Fix the Nginx Configuration (`/home/user/nginx.conf`):**
   We have a broken Nginx configuration. It currently points to the wrong upstream addresses and tries to use system directories requiring root. Modify `/home/user/nginx.conf` so that:
   - Nginx runs entirely as the local user (store pid, client_body_temp, etc., in `/home/user/nginx_temp/`).
   - Nginx listens on the proxy port specified in the architecture diagram.
   - Nginx load balances incoming requests across the two upstream backend ports specified in the diagram.

3. **Fix the C Backend (`/home/user/backend.c`):**
   The custom C server was written by a junior developer and has multiple issues causing 502s:
   - It doesn't accept the port as a command-line argument (it currently hardcodes 8080, which conflicts with Nginx). Modify it to take the port as `argv[1]`.
   - The `listen()` backlog is too small, causing Nginx connections to be dropped under load. Increase it to at least 1024.
   - It processes requests sequentially and has an artificial `sleep` making it incredibly slow. Fix the concurrency issue (e.g., by handling client connections in a separate thread, using `fork()`, or implementing a fast non-blocking response) and remove the sleep.
   - Ensure it responds to any request with exactly: `HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK`

4. **Write the Deployment Script (`/home/user/deploy.sh`):**
   Create a bash script that:
   - Compiles `backend.c` into an executable named `backend`.
   - Creates the `/home/user/nginx_temp/` directory.
   - Starts two instances of `./backend` in the background, bound to the two upstream ports from the diagram.
   - Starts Nginx using `nginx -c /home/user/nginx.conf`.
   - Ensure the script is executable (`chmod +x`).

Once you've implemented everything, run `./deploy.sh`. An automated load test will then evaluate your Nginx endpoint using `wrk` with 100 concurrent connections. To pass, the setup must achieve a throughput of > 2000 Requests/sec with exactly 0 non-2xx/3xx responses.