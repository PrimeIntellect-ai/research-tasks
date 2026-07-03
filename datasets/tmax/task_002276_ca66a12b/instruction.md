You are a Cloud Architect leading the migration of a legacy routing broker. We are moving off an old proprietary appliance, but the original documentation has been lost. 

You need to write a set of Bash scripts to extract the old configuration, start a new Bash-based routing daemon, and provide health monitoring.

Here is what you have to work with:

1. **Lost Configuration:** The only surviving record of the legacy appliance's network configuration is a screenshot located at `/app/config_snapshot.png`. It contains the target port the service must listen on (`BIND_PORT`) and the security token (`AUTH_TOKEN`) required by our internal microservices. You must extract these values programmatically (e.g., using `tesseract`).

2. **Legacy Database:** The actual routing map is locked behind a legacy interactive CLI tool located at `/app/legacy_admin_cli`. 
   - It requires an interactive login. The credentials are Username: `admin`, Password: `legacy2024`.
   - Upon successful login, it outputs a list of routing rules in the format `key:ip_address`.
   - You must write an Expect script or use `expect` within Bash to automate this login and save the extracted routing map to `/home/user/routes.txt`.

3. **The New Routing Daemon:**
   Write a Bash script `/home/user/start_daemon.sh` that acts as an idempotent service launcher.
   - It should terminate any existing instances of the daemon.
   - It should use `socat` to listen on the `BIND_PORT` (extracted from the image) and fork a Bash request handler for incoming HTTP requests.
   
   The request handler must implement the following simple HTTP behavior:
   - **`GET /health`**
     Response: `HTTP/1.1 200 OK` with body `OK`.
   - **`GET /lookup?service=<key>`**
     - Must check for the HTTP header `X-Auth-Token: <AUTH_TOKEN>` (using the token from the image).
     - If the token is missing or incorrect, respond with `HTTP/1.1 403 Forbidden`.
     - If the token is correct, read `/home/user/routes.txt`, find the IP for the requested `<key>`, and respond with `HTTP/1.1 200 OK` and the IP address as the body.
     - If the key is not found, respond with `HTTP/1.1 404 Not Found`.

4. **Health Monitor:**
   Write a script `/home/user/monitor.sh` that sends a request to `GET /health` on the extracted port. If it fails, it should exit with code 1; if successful, exit with code 0.

Ensure your `start_daemon.sh` is running and the service is actively listening in the background before you finish. Do not leave the daemon in the foreground, blocking the terminal. Use `socat` for the server implementation. All line endings in HTTP responses must use `\r\n`.