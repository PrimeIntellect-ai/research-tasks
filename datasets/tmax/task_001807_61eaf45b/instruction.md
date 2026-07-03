I need you to fix a broken health monitoring setup on our server. The monitoring wrapper script is currently failing silently due to environment misconfigurations and a broken directory structure. 

Here is the situation:
1. There is a Python health check script located at `/home/user/monitor/check_health.py`. It requires specific locale and timezone environment variables to parse logs correctly, but it is currently failing because the wrapper script doesn't set them.
2. The health check script expects to find an application log file via a specific symlink path: `/home/user/logs/current/app.log`. Currently, the `current` symlink is missing.

Your tasks are:
1. Create a symbolic link at `/home/user/logs/current` that points to the actual log directory: `/home/user/app_data/logs`. 
2. Edit the bash wrapper script at `/home/user/monitor/run_monitor.sh`. You need to modify it so that it exports the timezone variable `TZ=UTC` and the locale variable `LC_ALL=C` immediately before executing the Python script. 
3. After fixing the symlink and the wrapper script, run `/home/user/monitor/run_monitor.sh`.

If you have configured everything correctly, the Python script will execute successfully and generate a status file at `/home/user/monitor/status.txt` containing exactly the text: `HEALTHY: ALL CHECKS PASSED`. 

Do not modify the `check_health.py` script itself, as its checksum is monitored by another system. Only modify the environment/symlinks and the wrapper script.