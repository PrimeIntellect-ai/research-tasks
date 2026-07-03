You are the system administrator for our incoming email processing pipeline. Currently, our NGINX proxy is returning a 502 Bad Gateway error when receiving webhook payloads. Your goal is to restore the service, write a required text-filtering script, and set up a backup cron job. 

Perform the following tasks:

1. **Restore NGINX Configuration:**
   The current NGINX configuration at `/etc/nginx/sites-available/default` is corrupted. Someone made a backup before the corruption at `/var/backups/nginx/default.bak`. Restore this backup file to its original location and ensure NGINX is reloaded to apply the changes.

2. **Fix the Backend Service:**
   NGINX acts as a reverse proxy to our backend Python service, `mail-receiver.service`, which processes incoming emails. The service source code is provided as a vendored package at `/app/py-mail-processor-1.2.0/`.
   Currently, the backend service is failing to communicate with NGINX because of a configuration mismatch. Inspect the vendored package and the systemd unit file (`/etc/systemd/system/mail-receiver.service`). Fix the mismatch so the service binds to the correct port that NGINX expects (8080). After fixing it, restart the service and ensure it is running properly.

3. **Develop a Subject Filter Script:**
   The backend service requires an external script to sanitize email subjects. Write a Python script at `/home/user/email_filter.py` that reads exactly one line of text from standard input (representing the raw email subject), removes all characters *except* alphanumeric characters, spaces, and hyphens, and prints the sanitized string to standard output. 
   Make sure the file has execution permissions (`chmod +x`). 

4. **Configure Automated Log Backups:**
   The backend service logs to `/var/log/mail-receiver.log`. Create a cron job for the `user` account that copies this log file to `/home/user/backups/mail-receiver.log.bak` every day exactly at midnight (00:00). Ensure the `/home/user/backups/` directory exists.

Ensure all services are running and your Python script is thoroughly tested before finishing.