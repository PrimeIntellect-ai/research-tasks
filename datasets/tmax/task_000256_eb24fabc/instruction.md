You are an operations engineer troubleshooting a broken connectivity pipeline in our local development environment. Our architecture relies on an SSH jump server, a custom TCP router, and a backend data service. Currently, the end-to-end flow is completely broken.

Here is the setup, located in `/home/user/app/`:
1. **SSH Jump Server:** A local instance of SSH (`sshd`) running as the current user, listening on `127.0.0.1:2222`. It is configured to only allow public key authentication. However, connection attempts using the provided key (`/home/user/test_key`) are being silently rejected by the server. 
2. **TCP Router:** A small bash-based TCP router service running on `127.0.0.1:8080`. It uses a routing table located at `/home/user/app/router/routes.conf` to forward requests to backend services.
3. **Backend Service:** A backend API listening on `127.0.0.1:9090`.

Your objectives are as follows:
1. **Fix SSH Authentication:** Diagnose and resolve why the SSH server on port 2222 is rejecting key-based login for `/home/user/test_key`. The `sshd_config` file is located at `/home/user/app/ssh/sshd_config`. You must not disable `StrictModes`.
2. **Fix Network Routing:** The TCP router on port 8080 is currently rejecting connections to the `backend` service. Update its configuration in `/home/user/app/router/routes.conf` so that any traffic destined for the `backend` alias is correctly routed to `127.0.0.1:9090`.
3. **Automate Health Checks:** Create a scheduled task using bash. Write a script at `/home/user/health_check.sh` that continuously polls the backend service (via the TCP router at `127.0.0.1:8080`) every 5 seconds. 
   - It should send an HTTP GET request to `http://127.0.0.1:8080/api/status`.
   - It must append the HTTP status code and the timestamp to `/home/user/health.log` in the exact format: `[YYYY-MM-DD HH:MM:SS] STATUS: 200`.
   - Start this script in the background so it runs continuously.

Ensure that the SSH server and all other services are running and functional when you complete the task. An automated verifier will attempt an end-to-end flow by SSHing into the jump server, establishing a local port forward to the TCP router, and making an HTTP request to the backend.