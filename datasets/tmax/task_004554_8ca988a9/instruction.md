You are tasked with fixing a broken local web deployment and setting up a robust monitoring solution. Currently, requests to the local Nginx server are returning a 502 Bad Gateway error.

Here is the current state of the system:
- There is a project directory at `/home/user/deploy/`.
- The Nginx configuration file is located at `/home/user/deploy/nginx.conf`. It is configured to listen on port 8080 and reverse proxy requests to a backend Python application on port 5000.
- The backend application is a simple Python HTTP server located at `/home/user/deploy/app.py`. However, it is currently hardcoded to bind to port 5001, which causes the 502 error from Nginx.
- Additionally, `app.py` crashes on startup because it expects a configuration file at `/home/user/deploy/config.json` containing valid JSON, which is currently missing.

Your objectives are:
1. **Fix the Configuration:** Update `/home/user/deploy/nginx.conf` so that it proxies traffic to the correct backend port (5001).
2. **Fix the Backend Dependencies:** Create the missing `/home/user/deploy/config.json` file. It must contain the exact JSON: `{"status": "ok"}`.
3. **Start the Services:** 
   - Start the backend application (`python3 /home/user/deploy/app.py &`).
   - Start Nginx using the local configuration and prefix: `nginx -c /home/user/deploy/nginx.conf -p /home/user/deploy/`
4. **Create a Watchdog Script:** Write a robust Python script at `/home/user/watchdog.py`. This script must make an HTTP GET request to `http://127.0.0.1:8080/`. 
   - If the response status code is 200, it must append the exact string `UP` (followed by a newline) to `/home/user/status.log`.
   - If the request fails, times out, or returns any other status code (like 502), it must gracefully catch the error and append the exact string `DOWN` (followed by a newline) to `/home/user/status.log`.
5. **Schedule the Watchdog:** Configure the current user's crontab to execute `/home/user/watchdog.py` every minute. Use `python3` explicitly in the cron job.

Ensure all files are created with the exact names and paths specified. Do not require root access to run these commands.