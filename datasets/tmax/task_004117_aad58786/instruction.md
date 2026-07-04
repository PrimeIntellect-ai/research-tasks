We have a legacy web application consisting of an Nginx reverse proxy, a custom C FastCGI backend, and a Redis server for session management. The application currently suffers from several security issues, and we need you to act as a DevSecOps engineer to secure the environment.

The services and source code are located in `/home/user/app/`. There is a script `/home/user/app/start_services.sh` that compiles the C code and starts Nginx, Redis, and the FastCGI process. 

Your tasks are:

1. **Vulnerability Remediation (C Code):**
   The FastCGI backend source code is located at `/home/user/app/backend/server.c`. It contains two critical vulnerabilities:
   - An open redirect vulnerability in the login flow. The `redirect_url` parameter is currently trusted without validation. You must modify `server.c` to ensure that `redirect_url` only permits relative paths starting with a single slash (e.g., `/dashboard`), and defaults to `/home` if an invalid or external URL is provided.
   - A reflected Cross-Site Scripting (XSS) vulnerability on the error page. The `error_msg` parameter is reflected directly. You must HTML-entity encode the `error_msg` before printing it (specifically escaping `<`, `>`, `&`, `"`, and `'`).

2. **Content Security Policy (CSP):**
   Update the Nginx configuration file located at `/home/user/app/nginx/nginx.conf` to enforce a strict Content Security Policy. The CSP header must be added to all responses and configured exactly as follows:
   `default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; frame-ancestors 'none';`

3. **Log Parsing and Access Control:**
   We have suspected malicious activity. A security log file is located at `/home/user/app/logs/auth.log`. Write a shell command to parse this log, identify the IP address that has more than 10 failed login attempts, and configure Nginx (`/home/user/app/nginx/block.conf`, which is included by `nginx.conf`) to deny HTTP requests from this specific IP address using Nginx's `deny` directive.

4. **Network Policy:**
   Ensure the Nginx server listens on port 8080 (already configured). The Redis server currently binds to `0.0.0.0:6379`. Modify `/home/user/app/redis/redis.conf` to bind only to `127.0.0.1`.

Once you have made the changes, ensure all services are restarted using the `/home/user/app/start_services.sh` script. Leave the services running. Automated tests will verify the security of the application by sending HTTP requests to port 8080.