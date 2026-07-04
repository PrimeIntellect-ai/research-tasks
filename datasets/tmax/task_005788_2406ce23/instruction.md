You are acting as a capacity planner for a new microservice. Your team has just executed a staged deployment of the service to a local environment, but the monitoring endpoints are currently failing. Nginx is returning a 502 Bad Gateway error because the upstream unix socket path in the Nginx configuration is incorrect. 

Your tasks are to fix the deployment, gather capacity metrics, set up log rotation for the staging environment, and generate an automated capacity report email.

Follow these instructions carefully:

1. **Fix the Staged Deployment:**
   - The Nginx configuration for the staging environment is located at `/home/user/staging/nginx.conf`. 
   - The backend service is an existing Python script located at `/home/user/staging/app.py`.
   - Inspect `/home/user/staging/app.py` to determine the correct Unix socket path it binds to.
   - Edit `/home/user/staging/nginx.conf` and update the `proxy_pass` directive to point to the correct Unix socket path instead of the currently misconfigured one.
   - Start the backend service in the background: `python3 /home/user/staging/app.py &`
   - Start Nginx in the background using the fixed configuration: `nginx -p /home/user/staging -c /home/user/staging/nginx.conf`

2. **Generate Usage Metrics:**
   - As a capacity planner, you need baseline metrics. Generate exactly 5 successful requests to the local staging endpoint by running: `curl http://127.0.0.1:8080/plan` 
   - Ensure these requests return a 200 OK status (which confirms your Nginx socket fix is working).

3. **Configure Log Rotation:**
   - To prevent disk space issues on the staging server, set up a log rotation configuration.
   - Create a file at `/home/user/staging/logrotate.conf`.
   - It must be configured to rotate the log file `/home/user/staging/logs/access.log`.
   - The rotation policy must specify: `daily` rotation, keep exactly `5` rotated backups, and use `compress` to compress the rotated files.

4. **Generate the Capacity Report Email:**
   - Write a script in Python, Ruby, or Bash at `/home/user/analyze.py` (or `.rb` / `.sh`).
   - The script must read `/home/user/staging/logs/access.log`, which is in the default Nginx combined/main format.
   - The script must parse the log to calculate the total sum of "body bytes sent" (the 10th field in standard combined log format) across all requests.
   - The script must generate a valid RFC 822 email file saved to `/home/user/capacity_report.eml`.
   - The email file must contain the following headers and body structure:
     `To: capacity@example.com`
     `Subject: Staging Capacity Report`
     
     `Total bytes sent: <SUM>`
   - Replace `<SUM>` with the actual computed integer sum of bytes sent. 
   - Run your script so that `/home/user/capacity_report.eml` is successfully generated.