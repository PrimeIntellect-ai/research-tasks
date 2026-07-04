You are tasked with fixing a broken web application setup and creating a reliable process supervision mechanism. 

Currently, there is an Nginx configuration file at `/home/user/nginx/nginx.conf` designed to listen on port 8080 and proxy requests to a backend service. However, if you attempt to run it, querying `http://localhost:8080` will result in a 502 Bad Gateway error. The backend service script is located at `/home/user/app/backend.sh`.

Perform the following tasks to fix the system and ensure its reliability:

1. **Fix the Nginx Configuration**:
   Identify why Nginx returns a 502 error when proxying to the backend service. Correct the proxy port in `/home/user/nginx/nginx.conf` so it correctly points to the port the backend service actually listens on (examine `/home/user/app/backend.sh` to find the correct port).

2. **Create a Supervisor Script**:
   Write a Bash script at `/home/user/scripts/supervisor.sh`. This script must act as a process supervisor for the backend with the following requirements:
   - **Execution**: The script must be executable.
   - **Supervision**: It must execute `/home/user/app/backend.sh` in the foreground. If the backend script exits, the supervisor must immediately restart it in an infinite loop.
   - **Logging**: The stdout and stderr of the backend must be redirected to `/home/user/logs/backend.log`.
   - **Log Rotation**: Before starting (or restarting) the backend, the supervisor must check the size of `/home/user/logs/backend.log`. If the file exists and its size is strictly greater than 1024 bytes, rename it to `/home/user/logs/backend.log.old` (overwriting any previous backup) before starting the backend.
   - **Alerting (Simulated Email)**: If the backend exits with a non-zero exit code, the supervisor must append the exact line `Subject: Backend Crash Alert` to the file `/home/user/mail/alerts` before restarting the backend.

3. **Deploy and Verify**:
   - Start your supervisor script in the background.
   - Start Nginx using the fixed configuration: `nginx -p /home/user/nginx -c /home/user/nginx/nginx.conf`
   - Verify the setup by running `curl -s http://localhost:8080` and redirecting the exact output to `/home/user/success.txt`.

Ensure all directories mentioned above exist before trying to write to them. Do not use external process managers like systemd or supervisord; your Bash script must handle the supervision natively.