You are a deployment engineer tasked with rolling out an update to a local backend service. After the latest deployment, the system health checks are failing (simulating an HTTP 502 error) because the frontend proxy configuration is still pointing to the old Unix domain socket path of the backend daemon, whereas the backend configuration has been updated to use a new socket path.

Your objective is to fix the deployment configuration and write a robust health checker in C++ to verify the backend daemon is responsive.

Perform the following steps:

1. **Fix the Proxy Configuration:**
   - The backend configuration is located at `/home/user/app/server.conf`. It contains a key-value pair `BIND_PATH=<path_to_socket>`.
   - The proxy configuration is located at `/home/user/deploy/proxy.conf`. It currently contains a line resembling `proxy_pass http://unix:/path/to/old/socket.sock;`.
   - Write a shell script at `/home/user/update_config.sh` that uses text processing tools (like `awk`, `sed`, or `grep`) to extract the `BIND_PATH` value from `/home/user/app/server.conf` and dynamically replaces the old socket path in `/home/user/deploy/proxy.conf` with the new one.
   - Execute your script so that `/home/user/deploy/proxy.conf` is corrected.

2. **Write a C++ Health Checker:**
   - Write a C++ program at `/home/user/health_check.cpp`.
   - The program must accept exactly one command-line argument: the path to the Unix domain socket.
   - It should create an `AF_UNIX` socket, connect to the provided path, and send the string `"STATUS\n"` (exactly 7 bytes).
   - It must then read the response from the socket.
   - If the response contains the substring `"OK"`, the program must create/overwrite a file at `/home/user/health_report.log` with the exact text `"HEALTHY"` and exit with status code `0`.
   - If it fails to connect or does not receive `"OK"`, it should exit with a non-zero status code.

3. **Verify the Deployment:**
   - Compile your C++ program to `/home/user/hcheck` (e.g., using `g++ -std=c++17 -o /home/user/hcheck /home/user/health_check.cpp`).
   - Run `/home/user/hcheck` passing the updated socket path (the one found in `/home/user/app/server.conf`).
   - Ensure that `/home/user/health_report.log` is successfully created with the required content.

Constraints:
- Do not hardcode the socket paths in your shell script; it must read from `/home/user/app/server.conf`.
- You do not need to restart any services; the backend daemon is already listening on the new socket path.