We have a local development environment set up for a Git webhook processor, but it is currently broken. Our Nginx reverse proxy is returning a 502 Bad Gateway error when trying to access the API. 

Your task is to diagnose and fix the network and configuration issues, fix the Go backend code, establish the correct directory structures, and configure log rotation. 

Here are the requirements to fix the system:

1. **Fix the Nginx Configuration**:
   - The Nginx configuration file is located at `/home/user/nginx.conf`. 
   - It is currently set up to proxy requests to our Go backend, but it's returning a 502 error when accessing `http://127.0.0.1:8080/health` and `http://127.0.0.1:8080/api/hook`.
   - Find the misconfiguration in `/home/user/nginx.conf` and update the `proxy_pass` directive to point to the correct backend port (9090).

2. **Fix and Run the Go Backend**:
   - The source code for the backend is at `/home/user/app/main.go`.
   - It has a bug where it is listening on the wrong port. Update it to listen on port `9090`.
   - Compile the application and start it in the background so it can process requests.

3. **Directory Structure and Symlinks**:
   - We serve public repositories via Nginx. There is a bare Git repository located at `/home/user/repos/project.git`.
   - Nginx expects the repositories to be accessible under `/home/user/public_html/repos`.
   - Create a symlink at `/home/user/public_html/repos` that points to `/home/user/repos` so that Nginx can serve static files if requested.

4. **Log Configuration and Rotation**:
   - The Go application is configured to append logs to `/home/user/logs/webhook.log`.
   - You need to create a logrotate configuration file at `/home/user/logrotate.conf` specifically for this log file.
   - The logrotate configuration must have the following settings for `/home/user/logs/webhook.log`:
     - Rotate daily
     - Keep exactly 5 backups (rotate 5)
     - Compress the old log files
     - Missing logs should be OK (missingok)
     - Do not rotate if empty (notifempty)

After fixing the Nginx config and the Go app, start Nginx using: `nginx -c /home/user/nginx.conf`. Start the Go backend.
Finally, verify your setup by running:
`curl -s -X POST http://127.0.0.1:8080/api/hook`
This should succeed (return 200 OK) and write "WEBHOOK_RECEIVED" to `/home/user/logs/webhook.log`.