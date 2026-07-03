You are a Site Reliability Engineer (SRE). We have a critical, but notoriously unstable, internal Python API running locally. 

Your task is to build an automated uptime monitoring and self-healing system for this service.

Here is the environment:
- The target service script is located at `/home/user/flaky_api.py`. It runs an HTTP server on `127.0.0.1:8080`.
- The service has a health check endpoint at `http://127.0.0.1:8080/health`.

You must complete the following objectives:

1. **Create a Watchdog Script:**
   Write a Python script at `/home/user/watchdog.py`. When executed, this script must:
   - Make an HTTP GET request to `http://127.0.0.1:8080/health` with a strict timeout of 2 seconds.
   - Determine the service state:
     - **HEALTHY**: Returns HTTP 200 OK.
     - **ERROR**: Returns any HTTP status code other than 200.
     - **TIMEOUT**: The request takes longer than 2 seconds.
     - **DOWN**: Connection refused (the process is not running).
   - If the state is ERROR, TIMEOUT, or DOWN, the script must:
     a) Terminate any existing `flaky_api.py` processes (using SIGKILL or SIGTERM).
     b) Restart the service by running `/usr/bin/python3 /home/user/flaky_api.py &` in the background (ensure it runs detached so the watchdog can exit).
     c) Append a log line to `/home/user/watchdog.log` in this EXACT format:
        `[YYYY-MM-DD HH:MM:SS] RESTART triggered. Reason: <STATE>` (where `<STATE>` is ERROR, TIMEOUT, or DOWN).
   - If the state is HEALTHY, do nothing and exit cleanly.

2. **Schedule the Watchdog:**
   Configure the current user's crontab to execute `/usr/bin/python3 /home/user/watchdog.py` every single minute.

3. **Configure Log Rotation:**
   Create a standard `logrotate` configuration file at `/home/user/watchrotate.conf` specifically for `/home/user/watchdog.log`.
   It must contain the following rules:
   - Rotate the log daily.
   - Keep exactly 5 rotated backups.
   - Compress the rotated files.
   - Do not throw an error if the log file is missing (`missingok`).
   - Create a new empty log file after rotation with permissions `0644`.

Ensure your watchdog script is executable and robust. Do not start the service yourself; the automated tests will start the service, simulate failures, and invoke your watchdog and crontab to verify behavior.