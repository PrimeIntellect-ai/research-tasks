You are an engineer tasked with hardening the configuration and monitoring for a custom C++ application suite. The suite consists of a background server and a health-check client, but they are currently failing to communicate due to a network configuration mismatch, and the logs are not being rotated.

The application files are located in `/home/user/app`:
- `server.cpp`: A C++ daemon that binds to an IP and port specified in `/home/user/app/config.env` and writes to `/home/user/app/server.log`.
- `client.cpp`: A C++ health checker that connects to the server based on `/home/user/app/config.env`.
- `/home/user/app/config.env`: Currently contains misconfigured networking environment variables.
- `/home/user/app/archive/`: A directory for rotated logs.

Your tasks:
1. **Network Configuration Fix**: The server binds to `127.0.0.2` but the client is attempting to reach it on a different loopback IP. Inspect and fix `/home/user/app/config.env` so the `CLIENT_TARGET_IP` matches the `SERVER_BIND_IP` (`127.0.0.2`), and ensure both use port `8888`.
2. **Compile**: Compile `server.cpp` to an executable named `server` and `client.cpp` to an executable named `client` inside `/home/user/app/`.
3. **Run the Server**: Start the `./server` process in the background. It will automatically read `config.env` and start writing to `server.log`.
4. **Process Monitoring and Log Rotation**: Create a bash script at `/home/user/app/monitor.sh`. The script must:
   - Check if the `server` process is running (e.g., using `pgrep`).
   - If it is NOT running, exit with status code 1.
   - If it IS running, perform a log rotation: copy the contents of `/home/user/app/server.log` to `/home/user/app/archive/server_rotated.log` and then empty (truncate) the original `/home/user/app/server.log`.
   - Finally, execute the `./client` binary and append its standard output to `/home/user/app/health.log`.

Make sure `/home/user/app/monitor.sh` is executable and run it once after starting the server.

Leave the `server` process running when you are finished.