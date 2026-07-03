I am an edge computing engineer deploying a resilient heartbeat service to our remote IoT devices. Our devices sometimes face transient network rejections (similar to an SSH config silently dropping connections). I need you to build a custom C-based heartbeat client, a Bash process supervisor that handles restarts and basic log rotation, and a health check script.

Please complete the following phases. All files must be created inside `/home/user/`.

**Phase 1: The C Heartbeat Client**
Write a C program at `/home/user/heartbeat.c` that does the following:
1. Reads the environment variable `HUB_PORT`.
2. Attempts to establish a TCP connection to `127.0.0.1` on the port specified by `HUB_PORT`.
3. If the connection fails, it prints exactly `CONNECTION_FAILED\n` to standard output and exits with status code `1`.
4. If the connection succeeds, it enters a loop that runs exactly 5 times. In each iteration, it:
   - Prints exactly `HEARTBEAT_SENT\n` to standard output.
   - Sends the string `PING\n` over the TCP socket.
   - Sleeps for 1 second.
5. After the 5 iterations, it gracefully closes the socket and exits with status code `2` (simulating a deliberate periodic reset).
6. Compile the code to an executable named `/home/user/heartbeat`. (Use standard libraries, e.g., `<stdio.h>`, `<stdlib.h>`, `<string.h>`, `<unistd.h>`, `<arpa/inet.h>`).

**Phase 2: Environment Setup**
Add a line to `/home/user/.bashrc` that exports the `HUB_PORT` variable set to `8888`.

**Phase 3: The Supervisor Script**
Write a Bash script at `/home/user/supervisor.sh` that acts as a process supervisor:
1. It must make sure the directory `/home/user/logs/` exists.
2. It must source `/home/user/.bashrc` to load the `HUB_PORT`.
3. It must run an infinite loop that executes `/home/user/heartbeat`.
4. The standard output of the heartbeat program must be appended to `/home/user/logs/edge.log`.
5. Every time the `heartbeat` process exits (regardless of the exit code), the supervisor must check the file size of `/home/user/logs/edge.log`. If the file size is strictly greater than 100 bytes, it must rename the file to `/home/user/logs/edge.log.old` (overwriting any previous `.old` file).
6. The supervisor must `sleep 1` before restarting the `heartbeat` process.
7. Make the script executable.

**Phase 4: The Health Check Script**
Write a Bash script at `/home/user/health_check.sh`:
1. It must check both `/home/user/logs/edge.log` and `/home/user/logs/edge.log.old`.
2. If the string `HEARTBEAT_SENT` appears in either file, the script should output `STATUS: OK` to standard output and exit with code `0`.
3. If the string does not appear in either file, or if the files don't exist yet, it should output `STATUS: FAIL` and exit with code `1`.
4. Make the script executable.

Do not background or start the supervisor yourself. Just leave the compiled binary and the scripts ready in `/home/user/`.