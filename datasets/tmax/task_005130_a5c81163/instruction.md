You are an infrastructure engineer tasked with automating the local deployment of a resilient microservice using bash and user-level tools (no root access available).

You have an initial setup in `/home/user/infra_project`. 
Inside this directory, there is a pre-existing `server.py` (a mock API listening on port 8080) and a `backup.tar.gz` containing an initial `data.json` file.

Your goal is to write a master script `/home/user/infra_project/deploy.sh` (and any associated scripts) that performs the following provisioning and management tasks:

1. **Backup/Restore Initialization**: 
   Before starting the server, your deployment must check if `/home/user/infra_project/data/data.json` exists. If it does not, extract `backup.tar.gz` such that the file ends up at exactly that path.

2. **Process Supervision**:
   Write a custom Bash supervisor script (`/home/user/infra_project/supervisor.sh`) that starts `python3 /home/user/infra_project/server.py`. 
   If `server.py` crashes or exits, the supervisor must immediately restart it. Every time a restart occurs (including the initial startup), append a line with the exact format `[YYYY-MM-DD HH:MM:SS] Starting server` to `/home/user/infra_project/logs/server.log`.

3. **Port Forwarding**:
   The API natively listens on 127.0.0.1:8080. Use `socat` to create a local port forward so that external traffic connecting to `127.0.0.1:9090` is forwarded to `127.0.0.1:8080`. This must run in the background.

4. **Connectivity Diagnostics**:
   Write `/home/user/infra_project/health_monitor.sh` which runs in the background. Every 1 second, it should attempt to connect to `http://127.0.0.1:9090/health` (using `curl`). 
   - If the curl command succeeds (exit code 0), append `OK` to `/home/user/infra_project/logs/health.log`.
   - If it fails, append `FAILED` to `/home/user/infra_project/logs/health.log`.

5. **Log Rotation**:
   Create a local logrotate configuration at `/home/user/infra_project/logrotate.conf` to manage all `.log` files in `/home/user/infra_project/logs/`.
   Requirements: rotate daily, keep 3 rotations, compress old logs, missing ok, and do not use root permissions. Set it up so it uses a local state file at `/home/user/infra_project/logrotate.status`.

**Execution:**
Your `deploy.sh` script must launch the initialization, the supervisor (in the background), the port forward (in the background), and the health monitor (in the background). 

Make sure all scripts have the correct execution permissions. Do not use systemd or cron, as you do not have root privileges. The automated test will execute `deploy.sh`, test the API endpoints, artificially kill the server to test your supervisor, and manually trigger your `logrotate.conf` to verify rotation.