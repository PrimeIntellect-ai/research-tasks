You are an administrator tasked with fixing a broken local deployment of a Python backend service. Currently, the local Nginx instance is configured to serve the app, but making a request to it results in a 502 Bad Gateway error. 

Here is the current state of the system:
- The deployment directory is `/home/user/app`. Releases are stored in `/home/user/app/releases/`.
- The active release is supposed to be linked via a symlink at `/home/user/app/current`.
- The Python backend application is located in the active release directory as `app.py`. It runs on port `8080` and binds strictly to IPv4 (`127.0.0.1`).
- The Nginx configuration is located at `/home/user/nginx.conf` and is configured to listen on port `8443`.

Please resolve the issues by completing the following steps:

1. **Fix the Directory Structure**: The symlink `/home/user/app/current` is broken (pointing to a non-existent release `v2`). Update the symlink to point to the existing release directory `/home/user/app/releases/v1`.
2. **Fix Network Routing Issue**: Nginx is currently configured to proxy traffic to `http://localhost:8080`. However, the local system resolves `localhost` to the IPv6 loopback (`::1`) first, while the Python app only binds to the IPv4 loopback (`127.0.0.1`). Modify `/home/user/nginx.conf` to explicitly proxy to `http://127.0.0.1:8080`.
3. **Setup TLS**: The Nginx configuration has placeholders for SSL certificates. Generate a self-signed certificate and private key. Save the certificate as `/home/user/cert.pem` and the key as `/home/user/key.pem`. Uncomment and update the relevant SSL lines in `/home/user/nginx.conf` to use these files.
4. **Start the Services**: 
   - Start the backend application by running `python3 /home/user/app/current/app.py` in the background.
   - Start Nginx using the custom configuration: `nginx -c /home/user/nginx.conf`.
5. **Implement a Health Monitor**: Write a Python script at `/home/user/health_monitor.py`. This script must:
   - Make an HTTPS GET request to `https://127.0.0.1:8443/` (ensure it ignores self-signed SSL certificate warnings).
   - If the HTTP response status code is 200, append the exact string `STATUS: UP` (followed by a newline) to `/home/user/health.log`.
   - If the request fails or returns any other status, append `STATUS: DOWN` to `/home/user/health.log`.
   - Run your script once so that the log file is created and populated.

Ensure all file paths are exact and the final `/home/user/health.log` exists with the correct output.