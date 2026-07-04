You are acting as a site administrator for a custom User Account Management system. The system consists of two C-based microservices: a backend database simulator (`backend`) and a frontend API (`frontend`). 

Currently, the services cannot communicate due to a network misconfiguration, and we lack proper process management, health monitoring, and log rotation. You need to fix the code, configure the environment, and write the necessary bash scripts to manage these services.

Here is the current state of the system in `/home/user/`:
- `/home/user/src/backend.c`: The backend service code. (Already perfect, do not modify).
- `/home/user/src/frontend.c`: The frontend service code. It has a network misconfiguration.
- `/home/user/config/system.env`: A configuration file containing environment variables.
- `/home/user/logs/`: Directory for log files.
- `/home/user/run/`: Directory for PID files.

**Step 1: Fix the Network Misconfiguration**
The `frontend.c` is currently hardcoded to connect to the backend at an unreachable IP (`192.168.99.99`). 
Modify `/home/user/src/frontend.c` so that it dynamically reads the backend IP and PORT from the environment variables `BACKEND_IP` and `BACKEND_PORT` (which will be sourced from `/home/user/config/system.env`).
If the environment variables are not set, it should exit with code 1.

**Step 2: Build the Services**
Compile both C programs.
- Output the backend binary to `/home/user/bin/backend`
- Output the frontend binary to `/home/user/bin/frontend`
Ensure the `/home/user/bin` directory exists.

**Step 3: Process Lifecycle Management**
Write a bash script at `/home/user/start_services.sh` that does the following:
1. Sources `/home/user/config/system.env`.
2. Starts the backend service in the background. It listens on `BACKEND_IP` and `BACKEND_PORT`. Redirect its stdout/stderr to `/home/user/logs/backend.log`.
3. Saves the backend's PID to `/home/user/run/backend.pid`.
4. Starts the frontend service in the background. It listens on `FRONTEND_PORT` (bound to `127.0.0.1`). Redirect its stdout/stderr to `/home/user/logs/frontend.log`.
5. Saves the frontend's PID to `/home/user/run/frontend.pid`.

**Step 4: Health Check & Monitoring**
Write a script at `/home/user/monitor.sh` that checks the health of the frontend system.
The frontend service responds to the exact string `HEALTH_CHECK\n` sent over TCP.
The script must:
1. Source `/home/user/config/system.env`.
2. Use `nc` (netcat) or `bash`'s `/dev/tcp` to send the string `HEALTH_CHECK\n` to `127.0.0.1` on `FRONTEND_PORT`.
3. Read the response. If the response contains the word `OK`, append the exact line `[YYYY-MM-DD HH:MM:SS] STATUS: HEALTHY` to `/home/user/logs/health.log` (use the `date "+%Y-%m-%d %H:%M:%S"` format).
4. If it fails or times out (use a 2-second timeout), append `[YYYY-MM-DD HH:MM:SS] STATUS: UNHEALTHY`.

**Step 5: Log Rotation**
Write a script at `/home/user/rotate.sh` that manually implements log rotation for `/home/user/logs/health.log`.
If `/home/user/logs/health.log` has strictly more than 5 lines, the script must:
1. Move `health.log.1` to `health.log.2` (if it exists).
2. Move `health.log` to `health.log.1`.
3. Create a new, empty `health.log`.

Do not start the services or run the monitor/rotate scripts yourself. Just create the binaries and the three bash scripts (`start_services.sh`, `monitor.sh`, `rotate.sh`), and make sure the scripts are executable. The automated test will execute them to verify your work.