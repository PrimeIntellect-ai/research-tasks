You are a deployment engineer tasked with fixing a custom health-check server and implementing a lightweight deployment and process supervision system using only bash and standard CLI tools.

Currently, there is a C source file at `/home/user/health_server.c` that acts as a basic TCP server listening on port 9090 and returning a simple "OK" HTTP response. However, it currently exits after handling a single connection.

Your task consists of three parts:

1. **Fix the C Application**: 
   Modify `/home/user/health_server.c` so that it handles multiple connections in a loop rather than exiting after the first one. It must cleanly handle connections and continue listening on port 9090. Do not change the response string.

2. **Process Supervisor**:
   Create a bash script at `/home/user/supervisor.sh`. This script must:
   - Run in the foreground and execute `/home/user/health_server`.
   - Automatically restart the `health_server` process if it exits or is killed (with a 1-second delay between restarts).
   - Write its own PID to `/home/user/supervisor.pid`.
   - Write the currently running `health_server` child process PID to `/home/user/server.pid`. Update this file every time the server is restarted.
   - Forward all standard output and standard error from the server to `/home/user/server.log`.

3. **Deployment Script**:
   Create a bash script at `/home/user/deploy.sh`. This script is meant to be run when `health_server.c` is updated. It must:
   - Compile `/home/user/health_server.c` to a temporary binary.
   - Atomically replace `/home/user/health_server` with the new binary (using `mv`).
   - Send a `SIGTERM` signal to the running server process using the PID stored in `/home/user/server.pid` so the supervisor automatically restarts the newly compiled binary.

Ensure that your scripts have the executable bit set. You do not need to start the supervisor in the background yourself; the automated test will start `/home/user/supervisor.sh &` to evaluate your solution.