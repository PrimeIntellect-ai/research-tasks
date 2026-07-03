You are a monitoring specialist and system administrator. We are trying to deploy a local Python web application behind an Nginx reverse proxy running entirely in user space, but the application is currently returning a 502 Bad Gateway error. We also lack proper process management and monitoring.

Your task is to fix the deployment, implement process supervision, and write a robust monitoring script that generates offline "email" alerts if the service fails.

Here are your requirements:

1. **Fix the 502 Error**: 
   - Nginx is configured in `/home/user/nginx/nginx.conf` and listens on `127.0.0.1:8080`.
   - The upstream Python application is located at `/home/user/app/app.py` and is designed to listen on a Unix domain socket at `/home/user/app/app.sock`. 
   - Identify why Nginx is returning a 502 (assume the Nginx configuration has a misconfigured socket path) and correct the configuration file in `/home/user/nginx/nginx.conf`. Nginx must run as the current user.

2. **Setup Process Supervision**:
   - Create a Supervisor configuration file at `/home/user/supervisord.conf`.
   - Configure it to manage both the Python application (`python3 /home/user/app/app.py`) and Nginx.
   - Nginx must be started in the foreground (e.g., `nginx -p /home/user/nginx -c /home/user/nginx/nginx.conf -g 'daemon off;'`).
   - Both programs should be configured with `autostart=true` and `autorestart=true`.

3. **Develop a Monitoring and Alerting Script**:
   - Write a robust monitoring script in Python at `/home/user/monitor.py`.
   - The script must continuously check the Nginx endpoint `http://127.0.0.1:8080/` every 2 seconds.
   - If the HTTP response status code is anything other than `200` (e.g., if the upstream crashes and Nginx returns `502`), the script must immediately generate an email alert.
   - The alert must be saved as a text file in the directory `/home/user/alerts/` (create this directory).
   - The filename must be `alert_<timestamp>.eml` where `<timestamp>` is the current Unix epoch time (integer).
   - The contents of the `.eml` file must exactly match this RFC 5322-like format:
     ```
     To: admin@local.dev
     From: monitor@local.dev
     Subject: Alert - HTTP <STATUS_CODE>

     The web server returned HTTP status <STATUS_CODE>.
     ```
   - Make sure your script handles HTTP connection errors gracefully (e.g., if Nginx is entirely down, treat it as a `000` status code).

Do not start the supervisor daemon in the background permanently; just ensure all configuration files and scripts are perfectly prepared and tested so that running `supervisord -c /home/user/supervisord.conf` and `python3 /home/user/monitor.py` works seamlessly. Leave the files correctly configured at the specified paths.