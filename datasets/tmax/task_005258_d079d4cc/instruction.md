You are a deployment engineer rolling out a new user-space networking and monitoring stack for a lightweight API update. Since you do not have root access, you must build this deployment using standard Bash utilities and user-space tools.

Your objective is to orchestrate a deployment phase by writing automated scripts to handle port forwarding, health checking, log rotation, and storage monitoring. 

Please perform the following steps:

1. **Environment Setup:**
Create the following directories:
- `/home/user/run`
- `/home/user/logs`
- `/home/user/alerts`

2. **User-Space Port Forwarding:**
Write a deployment script named `/home/user/deploy.sh` (make sure it is executable). When executed, this script must:
- Start a process in the background using `socat` that listens on TCP port `8080` (on `127.0.0.1`) and forwards all incoming traffic to TCP port `9090` (on `127.0.0.1`).
- Save the exact Process ID (PID) of this `socat` background process into the file `/home/user/run/forwarder.pid`.

3. **Health Check Script:**
Create an executable Bash script named `/home/user/health_check.sh`. When executed, it must:
- Perform an HTTP GET request to `http://127.0.0.1:8080/` using `curl` (use a max timeout of 2 seconds).
- If the curl command succeeds and returns an HTTP status code of 200, append the exact string `[$(date +%s)] STATUS: OK` to `/home/user/logs/health.log`.
- If the curl command fails or returns any other HTTP status, append the exact string `[$(date +%s)] STATUS: FAIL` to `/home/user/logs/health.log`.
*(Note: A dummy web server will be running on port 9090 for verification).*

4. **Log Rotation Configuration:**
Create a configuration file for `logrotate` at `/home/user/logrotate.conf`. It must be configured to manage `/home/user/logs/health.log` with the following rules:
- Rotate whenever the file size exceeds `10k`.
- Keep exactly `3` backup rotations.
- Do not use any paths requiring root.

5. **Storage Monitoring Script:**
Create an executable Bash script named `/home/user/storage_monitor.sh`. When executed, it must:
- Calculate the total disk usage of the directory `/home/user/logs` in bytes (you can use `du -sb`).
- If the total size is strictly greater than 51200 bytes, write the exact string `QUOTA_EXCEEDED` to `/home/user/alerts/quota.txt` (overwriting any previous contents).
- If the total size is 51200 bytes or less, write the exact string `QUOTA_OK` to `/home/user/alerts/quota.txt` (overwriting any previous contents).

Finally, execute `/home/user/deploy.sh` so the port forwarder is actively running.