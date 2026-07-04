You are an unprivileged system administrator troubleshooting a broken web application stack. 

There is an Nginx server configured to proxy requests to a Python background application. However, any requests to the Nginx server on port 8080 currently return a 502 Bad Gateway error. The root cause is a path issue in the startup script that causes the Python app to write its Unix domain socket to the wrong location, preventing Nginx from communicating with it. Additionally, the log rotation mechanism is missing.

Your task is to fix the startup script, correct the Nginx configuration, and write a Python script for log rotation.

Here are the specific requirements:

1. **Fix the Application Startup Script**: 
   The script `/home/user/app/start_app.sh` is supposed to start the Python application `/home/user/app/server.py`. Because it might be executed from arbitrary directories (like via cron), it currently drops the application socket (`app.sock`) and log file (`app.log`) in whatever directory it was executed from. 
   Update `/home/user/app/start_app.sh` so that it always changes the working directory to `/home/user/app` before executing the Python script, ensuring `app.sock` and `app.log` are always created inside `/home/user/app/`.

2. **Fix the Nginx Configuration**:
   The Nginx configuration file at `/home/user/nginx/nginx.conf` is trying to proxy traffic to the wrong socket path. Modify the `proxy_pass` directive in the `location /` block to point to the correct Unix socket path: `http://unix:/home/user/app/app.sock`.
   Additionally, add a rule to the Nginx configuration to block access to the `/admin` path by returning a `403 Forbidden` status code.

3. **Implement Log Rotation in Python**:
   Write a Python script at `/home/user/app/rotate_logs.py`. When executed, this script must:
   - Check if `/home/user/app/app.log` exists.
   - If it exists, rename it to `/home/user/app/app.log.archive` (overwriting any previous archive).
   - Create a new, empty file at `/home/user/app/app.log`.
   - Set the permissions of the new `app.log` file to `0644`.

4. **Start the Services**:
   - Run your fixed `/home/user/app/start_app.sh` to start the Python server.
   - Start Nginx using the fixed configuration: `nginx -c /home/user/nginx/nginx.conf`
   - Run your log rotation script: `python3 /home/user/app/rotate_logs.py`

Once you have completed all steps, verify that `curl http://127.0.0.1:8080/` returns successfully and does not throw a 502, and that `curl http://127.0.0.1:8080/admin` returns a 403. Leave the background services running so the automated test can verify them.