You are a platform engineer managing a CI/CD pipeline. We need to securely proxy real-time build logs from an internal log-streaming service to the developers. The logs are streamed over WebSockets, and the backend service requires a specific checksum header to verify the proxy's authorization.

Your task is to dynamically generate an Nginx configuration file using a C program that calculates this required checksum.

1. There is a binary file located at `/home/user/runner_id.bin`.
2. Write a C program at `/home/user/calc_proxy.c` that:
   - Reads the entire contents of `/home/user/runner_id.bin`.
   - Calculates the CRC32 checksum of the file's contents (you must use the `zlib` library).
   - Prints a complete, syntactically valid Nginx configuration file to standard output.
3. The printed Nginx configuration must meet these requirements:
   - Include the necessary minimal rootless Nginx boilerplate so it can be tested without `sudo` (e.g., `events {}`, `http {}` blocks, and setting `pid`, `access_log`, and `error_log` to paths in `/tmp/`).
   - Define a `server` block listening on port `8080`.
   - Define a `location /logs` block that acts as a reverse proxy forwarding requests to `http://127.0.0.1:9090`.
   - Configure the reverse proxy to properly handle **WebSocket connections** (you must configure the standard `Upgrade` and `Connection` headers for WebSocket proxying).
   - Inject a custom header into the proxied request named `X-Runner-Checksum` containing the integer value of the calculated CRC32 checksum.
4. Compile your C program. Ensure you configure your build command to link the required libraries.
5. Run your compiled program and redirect its output to `/home/user/nginx_ws.conf`.
6. Verify your generated Nginx configuration is valid by running `nginx -t -c /home/user/nginx_ws.conf`.

Ensure the final configuration file exists at `/home/user/nginx_ws.conf` and successfully passes the Nginx syntax check. Do not start the Nginx server daemon, just ensure the configuration file is generated and valid.