You are tasked with fixing a broken transformation pipeline on a Linux system. The previous administrator left the system in a broken state, and currently, the main Nginx endpoint is returning a 502 Bad Gateway error. 

The system consists of three parts:
1. A local Nginx instance running on port 9090, serving as a reverse proxy. Its configuration is located at `/home/user/app/nginx.conf`.
2. A Python backend server `/home/user/app/server.py` that listens for HTTP requests, extracts the body, and pipes it to a backend data transformer via `stdin`.
3. A Rust-based data transformer. The original source code was lost, but a reference binary exists at `/home/user/oracle_transformer`.

Your objectives are:

1. **Restore the Rust Transformer:**
   Write a Rust program in `/home/user/app/src/main.rs` that reads from standard input (stdin) and writes to standard output (stdout). Its behavior must be bit-for-bit identical to the `/home/user/oracle_transformer` binary. 
   *Hint: The oracle performs a standard Run-Length Encoding (RLE) on uppercase alphabetic characters (e.g., input `AABBBC` becomes `2A3B1C`). Any non-uppercase-alphabetic characters should be passed through unchanged.*
   Compile your Rust program and place the executable at `/home/user/app/transformer`.

2. **Fix and Supervise the Backend:**
   The Python backend (`/home/user/app/server.py`) is currently not running. It requires an environment variable `TRANSFORMER_PATH=/home/user/app/transformer` to function correctly.
   Create a user-level Systemd service file at `/home/user/.config/systemd/user/backend.service` to run this Python script, ensuring it restarts automatically if it crashes. Enable and start the service so it listens on port 8080.

3. **Fix Nginx Configuration:**
   The Nginx configuration at `/home/user/app/nginx.conf` has a routing error causing the 502 Bad Gateway. Identify and fix the `proxy_pass` directive so that POST requests to `http://127.0.0.1:9090/transform` are correctly forwarded to the Python backend. Reload Nginx to apply changes (Nginx is started via `/usr/sbin/nginx -c /home/user/app/nginx.conf -p /home/user/app/`).

4. **Setup Health Monitoring:**
   Create a bash script at `/home/user/app/healthcheck.sh` that sends a POST request with the body `XYZ` to `http://127.0.0.1:9090/transform`. If the response is `1X1Y1Z`, it should append "OK" along with the current Unix timestamp to `/home/user/app/status.log`. Configure a cron job for the user `user` to run this script every minute.

Ensure the entire pipeline works end-to-end. An automated test will send thousands of random strings to the Nginx endpoint and directly to your compiled Rust binary to verify exact equivalence with the oracle.