I am trying to set up a local reverse proxy using Nginx to serve a Go API, but whenever I try to access the Nginx server, I get a 502 Bad Gateway error. Additionally, I realized I need the service to run over HTTPS, but Nginx is currently only set up for HTTP.

Here is the current state of my environment:
- There is a Go application located at `/home/user/app/main.go`. It currently fails to start because it attempts to bind to port 80, which requires root privileges.
- Nginx is configured via `/home/user/nginx/nginx.conf` to listen on port 8080 (HTTP) and proxy requests to `http://127.0.0.1:9090`.

Your task is to fix the environment without using root access:

1. **Fix and Run the Go Backend:** Modify `/home/user/app/main.go` so that the HTTP server listens securely on `127.0.0.1:9090`. The server must respond to requests on the `/api` endpoint with the exact string `"Go Backend Online"`. Compile the Go application to `/home/user/app/main` and start it in the background.

2. **Configure TLS:** Generate a self-signed RSA TLS certificate and private key. Save them to `/home/user/certs/server.crt` and `/home/user/certs/server.key`.

3. **Update Nginx:** Modify `/home/user/nginx/nginx.conf` to:
   - Remove the HTTP listener on port 8080.
   - Add an HTTPS listener on port 8443.
   - Use the generated TLS certificate and key from Step 2.
   - Ensure it still proxies requests for `/api` to the Go backend.
   - Note: Nginx must be run as the local user (we will use `nginx -c /home/user/nginx/nginx.conf`).

4. **Process Monitoring Script:** Create an idempotent bash script at `/home/user/monitor.sh` (ensure it has executable permissions). When run, this script must:
   - Check if the Go binary (`/home/user/app/main`) is running and listening on port 9090. If not, start it in the background.
   - Check if Nginx is running with the custom config file. If not, start it using `nginx -c /home/user/nginx/nginx.conf`.

5. **Verification:** Start both services using your script, then run `curl -k https://127.0.0.1:8443/api` and redirect the output to `/home/user/success.txt`.