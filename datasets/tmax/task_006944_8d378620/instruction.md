You are tasked with setting up a lightweight, idempotent deployment and monitoring system for a custom Python application. You do not have root access, so all tools and scripts must run in user space. 

Please complete the following steps:

1. **The Application (`/home/user/app/app.py`)**
   Write a basic Python HTTP server that listens on `127.0.0.1` port `8080`.
   - It must respond to GET requests at the `/health` endpoint with an HTTP 200 status code and the text `OK`.
   - It should run continuously until explicitly killed.

2. **The Idempotent Deployer (`/home/user/deploy.py`)**
   Write a Python script that robustly manages the application's lifecycle.
   - It must ensure the directories `/home/user/app` and `/home/user/logs` exist, creating them if they do not.
   - It must check if the application is currently running by reading `/home/user/app/app.pid`.
   - If the process is already running (the PID is active), it should do nothing and exit gracefully.
   - If the process is not running (or the PID file doesn't exist), it must start `app.py` in the background, detach it so it continues running after the script exits, and write the new process ID to `/home/user/app/app.pid`.

3. **The Watchdog (`/home/user/watchdog.py`)**
   Write a Python script that acts as a health check.
   - It should send an HTTP GET request to `http://127.0.0.1:8080/health` with a 2-second timeout.
   - If it receives an HTTP 200 response, it must append exactly this line to `/home/user/logs/watchdog.log`:
     `[YYYY-MM-DD HH:MM:SS] STATUS: OK` (Replace with the current UTC timestamp).
   - If the connection is refused, times out, or returns a non-200 status, it must gracefully catch the error, execute `python3 /home/user/deploy.py` to restart the app, and then append exactly this line to `/home/user/logs/watchdog.log`:
     `[YYYY-MM-DD HH:MM:SS] STATUS: RESTARTED`

4. **Execution and Verification**
   To prove your system works, execute the following sequence of actions in the terminal:
   - Run `python3 /home/user/deploy.py` to start the app.
   - Run `python3 /home/user/watchdog.py` (This should log an OK status).
   - Manually kill the running `app.py` process.
   - Run `python3 /home/user/watchdog.py` (This should detect the failure, trigger a restart, and log the RESTARTED status).

Ensure the final state of the system has the application running and the watchdog log file properly formatted with both events.