You are acting as a network engineer troubleshooting a connectivity monitoring script. 

We have a cron job that runs a Python script (`/home/user/scripts/monitor.py`) every minute. However, the cron job is failing to produce the expected results due to environment differences. Specifically, it fails to find our custom network diagnostic tool, writes its output to the wrong directory (because cron runs in the user's home directory by default instead of the script directory), and logs timestamps in UTC instead of our local datacenter timezone.

Your task is to fix the Python script so that it is robust enough to run correctly via cron. 

Here is what you need to do:
1. Modify `/home/user/scripts/monitor.py` so that it correctly calls our custom executable `/home/user/bin/netcheck`. Currently, it just calls `netcheck` and fails because `/home/user/bin` is not in cron's `PATH`.
2. Update the script so that it explicitly appends its log output to the absolute path `/home/user/network_logs/status.log`, regardless of what the current working directory is.
3. Update the timestamp generation in the Python script to log the time in the `America/New_York` timezone. You must use the built-in `zoneinfo` module (or `pytz` if installed) to ensure the timezone is strictly `America/New_York`.
4. The output written to `/home/user/network_logs/status.log` must be in the exact format: `[YYYY-MM-DD HH:MM:SS] [America/New_York] STATUS: <output of netcheck>`
5. After fixing the script, execute it manually once using `python3 /home/user/scripts/monitor.py` so that the log file is generated for our automated tests to verify.

Do not assume any root privileges. All files and directories already exist or should be created within `/home/user/`.