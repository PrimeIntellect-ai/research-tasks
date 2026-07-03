Hello! We have a background worker script at `/home/user/worker.sh` that was designed to run continuously, but it keeps failing and exiting immediately. I need you to diagnose and fix it, and then set up a health monitoring system for it.

Here are your tasks:
1. **Fix the Worker Script**: The script `/home/user/worker.sh` fails to run. Diagnose the issue (hint: check permissions and file paths it attempts to write to). Fix the script so it successfully logs its output to `/home/user/worker.log` instead of the current invalid path.
2. **Fix the Network Configuration**: The worker script tries to fetch data from a local API on port 8000. However, the service port was recently changed. There is a local HTTP server running on this machine in the background. Find out which port this local HTTP server is listening on, and update the URL in `/home/user/worker.sh` to use the correct port.
3. **Create a Health Check Script**: Write a new bash script at `/home/user/health.sh` (ensure it is executable). When executed, this script must:
   - Check if a process executing `worker.sh` is currently running.
   - Check if the local HTTP server port (the one you discovered in step 2) is accepting TCP connections.
   - If BOTH conditions are true, it must append exactly the text `OK` (on a new line) to `/home/user/health.log`.
   - If EITHER condition is false, it must append exactly the text `FAIL` (on a new line) to `/home/user/health.log`.
4. **Schedule the Health Check**: Configure a user cron job to execute `/home/user/health.sh` every minute.

Please write all scripts in Bash. You do not need to start `worker.sh` in the background permanently; our automated test suite will handle starting and stopping it to verify your health check script. Just ensure the code is fixed and the cron job is installed.