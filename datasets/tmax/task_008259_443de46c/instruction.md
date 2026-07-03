You are acting as a Site Reliability Engineer. We have a locally running microservice that has been experiencing network isolation issues, making it periodically unreachable. 

Your task is to create a Python-based watchdog script that monitors the service's network endpoint, manages its log file permissions, and is scheduled to run continuously via cron.

Specifically, you need to:
1. Write a Python script at `/home/user/uptime_monitor.py`.
2. The script must attempt an HTTP GET request to `http://localhost:8080/health`.
3. If the request is successful (HTTP 200), append the exact text `STATUS: UP` followed by a newline to the log file at `/home/user/service_status.log`.
4. If the request fails (e.g., Connection Refused, Timeout, or non-200 HTTP code), append the exact text `STATUS: DOWN` followed by a newline to `/home/user/service_status.log`.
5. Set the permissions of the script `/home/user/uptime_monitor.py` so that only the owner can read, write, and execute it (0700).
6. Ensure the log file `/home/user/service_status.log` exists and its permissions are strictly set so that only the owner can read and write to it (0600).
7. Schedule the script to run every minute by adding it to the current user's crontab. The cron job should execute the script using the absolute path `/home/user/uptime_monitor.py` with no additional arguments.

To complete this task, you will use the terminal to write the script, set the appropriate file permissions, and install the cron job. Do not start the service on port 8080 yourself; assume it is either running or down at any given time.