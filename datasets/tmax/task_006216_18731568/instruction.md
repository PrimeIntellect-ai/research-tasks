We have a fragile background worker script located at `/home/user/worker.py` that occasionally crashes. As a system administrator, you need to implement a user-space monitoring script to ensure this service stays alive.

Write a Python script at `/home/user/keepalive.py` that performs the following tasks:
1. Reads the PID from `/home/user/worker.pid`.
2. Checks if the process with that PID is currently running AND its command line contains `worker.py`. 
3. If the process is running correctly, the script should do nothing and exit gracefully with code 0.
4. If the process is NOT running (e.g., the PID file does not exist, the PID is dead, or the PID has been reused by a different process), your script must:
   - Start `/home/user/worker.py` in the background (detached from the script so `keepalive.py` can exit while `worker.py` continues running).
   - Write the new process ID to `/home/user/worker.pid`.
   - Append a log entry to `/home/user/monitor.log` in the exact format: `[YYYY-MM-DD HH:MM:SS] RESTARTED` (using the current UTC time).

Make sure `/home/user/keepalive.py` has executable permissions. You may use any standard library modules in Python.

Assume `/home/user/worker.py` already exists and is executable.