You are a Site Reliability Engineer (SRE). We have a custom monitoring system that is currently failing to log correctly due to environment variable and PATH differences when executed via its wrapper script. 

There are three main components already set up in `/home/user`:
1. `/home/user/bin/get_disk_usage` - A bash script that outputs the current disk usage percentage.
2. `/home/user/monitor_uptime.py` - A Python script intended to check a local service's uptime and record disk usage.
3. `/home/user/run_monitor.sh` - A bash wrapper script used to execute the Python script.

Your task is to fix the environment and the monitoring script to produce the correct log output:

1. **Start the Service:**
   Start a dummy HTTP server on `127.0.0.1:8000` serving the directory `/home/user/www` in the background.

2. **Fix the Wrapper Script:**
   Modify `/home/user/run_monitor.sh` so that before it runs `monitor_uptime.py`:
   - It appends `/home/user/bin` to the `PATH` environment variable.
   - It exports the environment variable `MONITOR_LOG_DIR` set to `/home/user/logs`.

3. **Complete the Python Monitor:**
   Edit `/home/user/monitor_uptime.py` using Python to do the following:
   - Perform an HTTP GET request to `http://127.0.0.1:8000`. If it succeeds (HTTP 200), the status is "UP". Otherwise, it is "DOWN".
   - Execute `get_disk_usage` using the `subprocess` module to get the disk usage percentage (it will work without an absolute path because you fixed the wrapper script).
   - Append a single line to `uptime.log` located inside the directory specified by the `MONITOR_LOG_DIR` environment variable. 
   - The log line must exactly match this format: `STATUS: <UP/DOWN>, DISK: <USAGE_OUTPUT>%`

4. **Run the Monitor:**
   Execute `/home/user/run_monitor.sh` once so that the log file is created and populated.

Do not use absolute paths for `get_disk_usage` inside the Python script. Ensure the Python script correctly reads the `MONITOR_LOG_DIR` environment variable.