You are a Linux Systems Engineer tasked with hardening and fixing a local user-space application stack. The application consists of a backend web service and a logging daemon. They are managed via systemd user services, but the current configuration is broken and insecure. 

You need to complete the following tasks without root access (using standard user privileges and `systemctl --user`):

1. **Fix Service Dependencies:**
   There are two services currently located in `/home/user/.config/systemd/user/`:
   - `log-sink.service`: Starts a local log sink on TCP port 9000.
   - `web-backend.service`: Starts a Python HTTP web server on TCP port 8080.
   
   Currently, `web-backend.service` fails to start because it tries to connect to the log sink before it is ready. Modify `web-backend.service` so that it explicitly specifies a dependency to start *after* and *requires* `log-sink.service`. Once fixed, reload the systemd user daemon and start both services successfully.

2. **Setup Port Forwarding (Reverse Proxy):**
   We do not want users connecting directly to port 8080. Create a new user-level systemd service file at `/home/user/.config/systemd/user/frontend-proxy.service`. 
   This service must use `socat` to listen on TCP port 8443 and forward all traffic to `127.0.0.1:8080`. 
   Configure it to start automatically, and start the service.

3. **Directory Structure & Symlinks:**
   The logs are generated in `/home/user/app/logs/`. 
   Create a symbolic link at `/home/user/app/current_logs` that points directly to the `/home/user/app/logs/` directory.

4. **Log Rotation Script:**
   Write a Bash script at `/home/user/app/rotate.sh`. Give it executable permissions.
   The script must do the following:
   - Check if the file `/home/user/app/logs/server.log` exists.
   - Rename `/home/user/app/logs/server.log` to `/home/user/app/logs/server.log.archive`.
   - Use `systemctl --user restart log-sink.service` to recreate the log file.
   - Append the string "ROTATION_COMPLETE" to a new file called `/home/user/app/rotation_status.txt`.

Verify your setup by ensuring `curl http://127.0.0.1:8443` returns a response, and running `./rotate.sh` creates the archive and status files.