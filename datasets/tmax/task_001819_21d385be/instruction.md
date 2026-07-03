You are a monitoring specialist tasked with setting up a custom health check and alerting system for a set of internal backend web servers. Since standard monitoring tools are unavailable in this restricted environment, you must build a lightweight solution using bash and C.

Your objective is to create a reliable setup script and a custom C-based TCP health monitor.

Here are your specific requirements:

1. **Backend Server Setup (`/home/user/launch.sh`)**:
   - Write a robust bash script at `/home/user/launch.sh`. Use `set -e` for error handling.
   - The script must start two background web servers using `python3 -m http.server` bound to `127.0.0.1` on ports `9001` and `9002`.
   - Wait 2 seconds to ensure the servers are fully initialized.
   - Compile a C program named `/home/user/monitor.c` into an executable at `/home/user/monitor`.
   - Run the compiled `/home/user/monitor` to check the status (both should be up).
   - Kill ONLY the server running on port `9002`.
   - Run the `/home/user/monitor` program a second time to detect the failure.

2. **C Health Monitor (`/home/user/monitor.c`)**:
   - Write a C program that attempts to establish a TCP connection to `127.0.0.1` on ports `9001` and `9002`.
   - If a connection to a port fails, the program must append an alert message to `/home/user/monitor.log` in the exact format: `ALERT: PORT <port> DOWN\n` (e.g., `ALERT: PORT 9002 DOWN`).
   - If the connection succeeds, it should close the socket cleanly and log nothing.

3. **Execution**:
   - Make `/home/user/launch.sh` executable and run it. 
   - Ensure the surviving server on port 9001 remains running in the background after the script finishes.

**Expected Final State**:
- `/home/user/launch.sh` and `/home/user/monitor.c` exist.
- A Python HTTP server is running on port `9001`.
- Port `9002` is dead.
- `/home/user/monitor.log` exists and contains exactly one line alerting that port 9002 is down.