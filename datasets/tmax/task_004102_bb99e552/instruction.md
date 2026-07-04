I am trying to prepare my Python web application deployment for our production servers, but the configurations are broken. The stack uses Nginx as a reverse proxy for a Python backend, both managed by user-level systemd services. 

Currently, the Nginx reverse proxy occasionally returns a 502 Bad Gateway because the proxy starts before the Python API is ready. Furthermore, the Python service fails to pick up the correct port environment variable, and the static files directory is missing its symlink.

Your task is to fix the configurations and extract some log metrics:

1. Fix the systemd dependencies: Edit `/home/user/.config/systemd/user/nginx.service`. Add the appropriate systemd directive in the `[Unit]` section to ensure it starts *after* `api.service`.
2. Fix the Python service environment: Edit `/home/user/.config/systemd/user/api.service`. The Python app relies on the `APP_PORT` variable. Ensure the service loads the environment file located at `/home/user/app.env`.
3. Fix the Nginx reverse proxy: Edit `/home/user/nginx/nginx.conf`. The `proxy_pass` directive is incorrectly pointing to port `8001`. Change it to point to the backend Python API at `http://127.0.0.1:8000`.
4. Create the missing symlink: Create a symbolic link at `/home/user/app/public` that points to `/home/user/shared_public`.
5. Process the error logs: I have an old log file at `/home/user/logs/nginx_access.log`. Use text processing tools (like awk/grep) to find all unique IP addresses that received a `502` HTTP status code. Save this unique list of IPs, one per line, to `/home/user/502_ips.txt`.

Ensure all file paths and modified configuration keys are exactly as requested. Since you are in a sandbox without systemd running, you only need to fix the configuration files—you do not need to execute `systemctl` commands.