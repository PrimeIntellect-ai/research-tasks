You are acting as a Site Reliability Engineer configuring a local uptime monitoring stack. You need to deploy a Python-based health check API behind a reverse proxy, ensure it is automatically supervised, and secure its configuration.

You do not have root access. All services must be run entirely in user-space.

Here are the requirements:

1. **Process Supervision**: 
   A Python API script exists at `/home/user/uptime_api.py`. It runs on port `9000`.
   Create a supervisor configuration file at `/home/user/supervisor/supervisord.conf`. Configure it to run `/home/user/uptime_api.py` using `python3`. Ensure that `autorestart=true` is set so the process restarts if it crashes.
   Start `supervisord` in the background using this configuration file.

2. **Reverse Proxy**:
   Create an HAProxy configuration file at `/home/user/haproxy/haproxy.cfg`. 
   Configure it to listen on `127.0.0.1:8080` (frontend) and forward all traffic to the Python API at `127.0.0.1:9000` (backend).
   Start the HAProxy process in the background as the current user using this config.

3. **Permission Management**:
   The HAProxy configuration file contains sensitive routing rules. Set the permissions of `/home/user/haproxy/haproxy.cfg` so that ONLY the owner has read permissions, and absolutely no other permissions are granted to anyone (chmod 400).

4. **Uptime Monitoring Script**:
   Write a Python script at `/home/user/check_health.py` that makes an HTTP GET request to `http://127.0.0.1:8080/health`.
   The script must write the raw JSON response body it receives into a log file exactly at `/home/user/health_log.txt`.

Execute the necessary commands, write the configuration files, start the services, and finally run your `check_health.py` script once to generate the `health_log.txt` file.