You are tasked with organizing and modernizing an old project that calculates mathematical polynomial rolling hashes. The project currently relies on a legacy Ruby script and a C source file, located in `/home/user/project`.

Your objective is to compile the shared library, translate the Ruby script's functionality into a Python-based web service, configure a reverse proxy to route traffic to it, and verify the entire pipeline.

Here are the specific requirements:

1. **Compile the Shared Library**:
   Compile the C source file `/home/user/project/math_ops.c` into a shared library named `libmathops.so` in the same directory.

2. **Translate and Modernize (Code Translation & Encoding)**:
   Analyze the provided `/home/user/project/legacy.rb` script to understand how it loads the shared library, decodes a hex-encoded string into raw characters, and calls the C function `compute_hash`.
   Write a Python script `/home/user/project/server.py` that implements a simple HTTP server on `127.0.0.1:8080`.
   - The Python server must use `ctypes` to load `libmathops.so` and define the appropriate ABI (Application Binary Interface) types.
   - It should expose a single endpoint: `GET /hash?data=<hex_string>`.
   - When this endpoint is hit, your Python code must decode the hex string into raw bytes/characters (handling the character encoding exactly as the Ruby script did), pass those bytes to the `compute_hash` C function, and return the integer result as plain text in the HTTP response.

3. **Reverse Proxy Configuration**:
   Create an Nginx configuration file at `/home/user/project/nginx.conf`.
   - The Nginx server must listen on `127.0.0.1:9090`.
   - It must act as a reverse proxy, intercepting any requests that start with `/api/` and forwarding them to the Python backend at `127.0.0.1:8080`.
   - The `/api/` prefix must be stripped before forwarding. For example, a request to `http://127.0.0.1:9090/api/hash?data=...` should be forwarded to `http://127.0.0.1:8080/hash?data=...`.
   - Because you do not have root access, configure Nginx to write its PID file to `/tmp/nginx.pid` and write access/error logs to `/dev/null` or `/tmp/`.

4. **Execution and Verification**:
   Start your Python server in the background.
   Start Nginx in the background using your configuration file (e.g., `nginx -c /home/user/project/nginx.conf -p /home/user/project`).
   Once both are running, use `curl` to send a GET request to the reverse proxy on port `9090` to compute the hash of the hex string `776f726c64`.
   Save the exact raw response body from the `curl` command to a log file at `/home/user/project/output.log`.