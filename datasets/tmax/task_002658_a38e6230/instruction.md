You are tasked with hardening a multi-service application environment and implementing a secure payload sanitizer. 

Currently, our application infrastructure is broken due to network misconfigurations between its components, and it lacks proper input validation, making it vulnerable to injection attacks. The application consists of three services managed locally via a startup script:
1. **Nginx** (Reverse Proxy) - Should listen on port 8080 and route traffic to the Backend.
2. **Backend API** (Python) - Should listen on port 9090, process requests, and cache data in Redis.
3. **Redis** (Cache) - Runs on the standard port 6379.

All application files and the startup script are located in `/home/user/app/`.

### Task 1: Fix Service Connectivity
The services currently fail to communicate because their configuration files specify incorrect ports.
1. Update `/home/user/app/nginx/nginx.conf` so the `proxy_pass` points to the Backend API on `127.0.0.1:9090`.
2. Update `/home/user/app/backend/config.json` so the Redis connection string points to `127.0.0.1:6379`.
3. Restart the services by killing existing instances and running `/home/user/app/start.sh`.

### Task 2: Build a C++ Payload Sanitizer
The Backend API is configured to shell out to a binary at `/home/user/app/filter/sanitizer` to check every incoming POST payload file before processing it. You must write this sanitizer in C++ and compile it to that exact location.

Requirements for `/home/user/app/filter/sanitizer`:
- It must take a single command-line argument: the absolute path to a text file containing the payload.
- It must read the contents of the file.
- It must exit with code `0` (Success) if the file is "clean".
- It must exit with code `1` (Reject) if the file contains any of the following malicious substrings (case-sensitive):
  - `../` (Path traversal)
  - `<script>` (XSS)
  - `DROP TABLE` (SQLi)
  - `$(whoami)` (Command Injection)
  - `; rm -rf` (Destructive command)
- Write your C++ source code to `/home/user/app/filter/sanitizer.cpp` and compile it using `g++`.

### Task 3: Health Monitoring Script
Create a bash script at `/home/user/app/health_monitor.sh` that checks if the `nginx`, `redis-server`, and `backend.py` processes are running. 
- If any of the three processes are missing, the script should execute `/home/user/app/start.sh` to bring the environment back up.
- Make sure the script is executable (`chmod +x`).

To complete this task, ensure the C++ sanitizer is compiled and functional, the configurations are corrected, and the services are running and intercommunicating.