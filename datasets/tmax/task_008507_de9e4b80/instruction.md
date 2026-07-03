Hello! I am an observability engineer setting up a local GitOps workflow for our dashboard configurations, and I need your help to build the pipeline. We want developers to push dashboard JSON files to a local Git server, which automatically validates them and serves them over a secure local web server. A background job will continuously monitor the health of this setup.

Please complete the following steps:

1. **Git Repository Setup:**
   - Create a bare Git repository at `/home/user/obs-gitops.git`.
   - Create a Python script as the `post-receive` hook at `/home/user/obs-gitops.git/hooks/post-receive`. Ensure it is executable.
   - The hook must read from standard input (`oldrev newrev refname`). When a push to the `refs/heads/main` branch occurs, the hook should inspect all files in the new commit (`newrev`).
   - For every file ending in `.json`, parse its contents. If it is valid JSON and contains a top-level key exactly named `"dashboard_id"`, extract it and save it to `/home/user/public_html/dashboards/` keeping its original filename. (Create this directory if it doesn't exist). Invalid files or files without `"dashboard_id"` should be ignored.

2. **Web Server & TLS Configuration:**
   - Generate a self-signed SSL certificate and private key at `/home/user/certs/cert.pem` and `/home/user/certs/key.pem`. Use `CN=localhost`.
   - Write a Python script at `/home/user/start_server.py` that starts a standard Python HTTP server serving the `/home/user/public_html/` directory on port `8443` with TLS enabled (using the generated cert and key).
   - Execute the server script so it runs in the background. Save the process ID (PID) of the web server to `/home/user/webserver.pid`.

3. **Scheduled Health Check:**
   - Write a Python script at `/home/user/health_check.py`.
   - When executed, this script should attempt an HTTPS GET request to `https://localhost:8443/` (ignoring SSL verification). 
   - If the server responds with a 200 OK (or directory listing 200 OK), the script should count the number of `.json` files present in `/home/user/public_html/dashboards/`.
   - It should then write a JSON file to `/home/user/public_html/health.json` with the following exact structure:
     `{"status": "up", "dashboard_count": <integer_count>}`
   - If the server cannot be reached, it should write:
     `{"status": "down", "dashboard_count": 0}`
   - Configure a cron job for the `user` to run `/home/user/health_check.py` every minute (`* * * * *`).

Ensure all scripts use `python3` and run correctly in the environment. Do not install any external Python packages (use standard libraries like `http.server`, `ssl`, `json`, `urllib.request`, `subprocess`, etc.).