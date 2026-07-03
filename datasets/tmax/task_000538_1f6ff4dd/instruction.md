You are an SRE tasked with restoring service to a critical internal API and setting up monitoring. The environment has a vendored Python backend application that is currently failing. You need to fix it, deploy it, put it behind a load balancer, and set up automated monitoring.

Here is what you need to do:

1. **Fix the Vendored Application**:
   The source code for the backend API is vendored at `/app/backend-api-2.1`. It is designed to run via Gunicorn and bind to a Unix socket. However, a recent faulty patch broke the configuration file (`gunicorn_conf.py`), causing it to bind to a hardcoded, incorrect path (`/tmp/broken_deploy.sock`).
   Fix the configuration so that it dynamically accepts the socket path via the `BIND_SOCKET` environment variable.

2. **Process Management**:
   Configure and start two instances of the backend application using user-level `systemd` services (`systemctl --user`). 
   - Instance 1 should bind to `/tmp/backend_1.sock`
   - Instance 2 should bind to `/tmp/backend_2.sock`
   Make sure these services are running and persist.

3. **Reverse Proxy and Load Balancer**:
   Create a custom Nginx configuration file at `/home/user/nginx.conf`. Configure Nginx to:
   - Run as a non-root user (do not use default system paths that require root for pid/logs).
   - Listen on `127.0.0.1:8080`.
   - Act as a reverse proxy and load balancer distributing traffic evenly between `/tmp/backend_1.sock` and `/tmp/backend_2.sock`.
   Start Nginx using this configuration in the background.

4. **Monitoring & Connectivity Diagnostics**:
   Write a Python script at `/home/user/monitor.py` that makes an HTTP GET request to `http://127.0.0.1:8080/ping`. 
   - If the endpoint returns an HTTP 200 status code, append the word `UP` to `/home/user/uptime.log`.
   - If it returns any other status code, times out, or cannot connect, append `DOWN` to `/home/user/uptime.log`.
   Ensure the log file is created.

5. **Scheduled Task**:
   Set up a user cron job to execute `/home/user/monitor.py` every minute.

Once you have completed these steps, inform the user. The automated system will evaluate your setup by running a load test against `http://127.0.0.1:8080/ping` and checking your success rate.