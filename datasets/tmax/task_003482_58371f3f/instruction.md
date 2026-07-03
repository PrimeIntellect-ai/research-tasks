You are a security compliance analyst tasked with generating audit trails and securing an internal microservice. 

Currently, an internal API runs locally at `127.0.0.1:8080` (you can simulate this with a simple python HTTP server or assume it will be running during tests). It processes sensitive data but lacks both transport security and proper token validation—specifically, it is vulnerable to accepting JWTs with the `none` algorithm.

You must build a security gateway and auditing layer using Nginx and a Bash CGI script.

Your objectives:

1. **Certificate Management & mTLS Setup**
   - Create a local Certificate Authority (CA).
   - Generate a server certificate for `localhost` and a client certificate for testing.
   - All private keys must reside in `/home/user/certs/` and the server's private key *must* have strict `0400` permissions.

2. **The Bash Audit & Validation Script**
   - Write a Bash CGI script at `/home/user/auth_filter.cgi`. Make it executable.
   - This script will be called by Nginx via FastCGI (using `fcgiwrap`) to validate every incoming request.
   - It must inspect the `HTTP_AUTHORIZATION` environment variable for a Bearer JWT.
   - **Vulnerability Mitigation:** If the JWT header specifies `"alg":"none"` (or any case-variant, base64url encoded), the script must reject the request by returning an HTTP `403 Forbidden` status.
   - **Audit Trail:** For all requests containing a JWT (valid or invalid), append an entry to `/home/user/audit.log` in this exact format:
     `[<YYYY-MM-DD HH:MM:SS>] AUDIT: Token with header <base64_header> evaluated. Status: <200 or 403>`
   - If the token is valid (not `none` algorithm), return HTTP `200 OK` so Nginx will allow the request through to the backend.

3. **Nginx Integration (`multi_service_compose`)**
   - Write an Nginx configuration file at `/home/user/nginx.conf`.
   - Nginx must listen on `0.0.0.0:8443` with HTTPS enabled.
   - It must require and verify client certificates (mTLS) using the CA you generated.
   - It must proxy successful requests to `http://127.0.0.1:8080`.
   - It must use the `auth_request` directive to trigger your `/home/user/auth_filter.cgi` for validation. You will need to spawn `fcgiwrap` on a local UNIX socket (e.g., `/home/user/fcgiwrap.sock`) and configure Nginx to route `/auth` to this socket using `fastcgi_pass`.

4. **Startup**
   - Provide a final script `/home/user/start_gateway.sh` that launches `fcgiwrap` in the background, starts `nginx` using your configuration, and ensures all permissions are correctly set. 

Ensure your Nginx config and CGI script handle standard HTTP headers correctly. Do not modify the backend service on port 8080.