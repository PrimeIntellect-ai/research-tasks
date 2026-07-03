You are acting as a Site Reliability Engineer. We have a local deployment of a multi-language application (a Python backend with an Nginx reverse proxy) running entirely in user space. Our synthetic monitoring is reporting that the Nginx endpoint at `http://127.0.0.1:8080` is constantly returning HTTP 502 Bad Gateway errors.

Your objectives are to diagnose the issue, fix the configuration, generate an incident report, and write an idempotent deployment script to automate the fix and establish a backup and log rotation strategy.

Here is the current state of the environment:
- The Nginx configuration file is located at `/home/user/nginx/conf/nginx.conf`. It routes traffic for port 8080 to a backend upstream via a Unix socket.
- The Python backend creates its socket at `/home/user/app/run/backend.sock`.
- Nginx logs are located at `/home/user/nginx/logs/access.log` and `/home/user/nginx/logs/error.log`.
- Application logs are located at `/home/user/app/logs/app.log`.

Perform the following tasks:

1. **Incident Analysis**: 
   Use text processing tools (e.g., `grep`, `awk`, `sed`) to parse `/home/user/nginx/logs/error.log`. Find the timestamps of the last 5 occurrences of the "502" error caused by a failed connection to an upstream socket.
   Write these exact 5 timestamps (date and time as they appear in the log, e.g., `2023/10/24 15:30:12`) to `/home/user/incident_report.txt`, one per line.

2. **Fix the Configuration**:
   Update `/home/user/nginx/conf/nginx.conf` so that the `proxy_pass` directive points to the correct backend socket path (`/home/user/app/run/backend.sock`).

3. **Automation & Backup Strategy**:
   Create a bash script at `/home/user/deploy.sh` that performs the following idempotently:
   - Backs up the current (fixed) `/home/user/nginx/conf/nginx.conf` to `/home/user/backup/nginx.conf.bak`. If the backup already exists, it should be overwritten. Ensure the `/home/user/backup` directory exists.
   - Verifies the `proxy_pass` path in `nginx.conf` is correct.
   - Implements a custom log rotation for `/home/user/app/logs/app.log` without using the system `logrotate` (since we lack root access). The `deploy.sh` script should rotate the log file by keeping up to 3 old versions (`app.log.1`, `app.log.2`, `app.log.3`), shifting them correctly (e.g., `.2` becomes `.3`), renaming the current `app.log` to `app.log.1`, and creating a new empty `app.log`.
   
Make sure `/home/user/deploy.sh` has executable permissions. You should execute `/home/user/deploy.sh` at least once to ensure the backup is created and the log rotation occurs.