You are a systems engineer diagnosing why a local network service is failing to start. 

We are developing a Go-based API for a VNC management portal. It is intended to run as a user-level background service, but it keeps failing during startup. You need to diagnose the environment, fix the application code, configure the necessary secure web server components, and automate its deployment.

Here are your instructions:
1. **Clear Port Conflicts**: The service needs to run on TCP port `8443`. Discover what process is currently binding to `127.0.0.1:8443` or `0.0.0.0:8443` and terminate it using standard bash text processing pipelines and process management commands.
2. **Fix Application Configuration**: The source code is located at `/home/user/vnc-api/main.go`. It is currently hardcoded to look for TLS certificates in `/etc/ssl/certs/`, which we don't have access to. Modify the Go code to point to `/home/user/vnc-api/certs/server.crt` and `/home/user/vnc-api/certs/server.key`.
3. **Web Server Setup (TLS)**: Generate a self-signed RSA 2048-bit TLS certificate and private key. Save them as `/home/user/vnc-api/certs/server.crt` and `/home/user/vnc-api/certs/server.key` respectively.
4. **Task Automation Script**: Create a bash script at `/home/user/deploy.sh` (ensure it is executable) that:
   - Compiles the Go code in `/home/user/vnc-api/` to a binary named `vnc-manager`.
   - Starts the `vnc-manager` binary in the background.
   - Redirects its stdout and stderr to `/home/user/vnc-api/api.log`.
5. **Verification**: Run your `deploy.sh` script. Once the service is running, use `curl` to make a GET request to `https://127.0.0.1:8443/status` (ignore TLS validation warnings). Save the exact raw JSON output to `/home/user/result.json`.

Make sure the final `/home/user/result.json` exactly matches the API's output.