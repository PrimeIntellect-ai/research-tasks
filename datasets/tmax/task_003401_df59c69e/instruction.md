You are an observability engineer tuning local dashboard metrics and log management on a Linux system. You need to configure log rotation, create a text-processing pipeline to extract metrics, and set up port forwarding for a dashboard healthcheck.

Perform the following tasks:

1. **Log Configuration and Rotation**:
   The service log file located at `/home/user/logs/api.log` is growing rapidly. 
   Create a custom `logrotate` configuration file at `/home/user/logrotate.conf` that specifically targets `/home/user/logs/api.log`.
   The configuration must enforce the following rules:
   - Rotate the log if its size exceeds 1k bytes.
   - Keep exactly 2 rotated backup logs.
   - Compress the rotated files, but use `delaycompress` so the most recently rotated file (`api.log.1`) remains uncompressed.
   Once configured, execute `logrotate` manually as the current user using your configuration file. You must specify a custom state file located at `/home/user/logrotate.state` so it does not attempt to write to the global root-owned state file.

2. **Text Processing Pipeline**:
   After a successful rotation, the most recent old log will be located at `/home/user/logs/api.log.1`.
   Write a bash script at `/home/user/parse.sh` that takes a file path as its first argument. The script must use standard text-processing tools (`grep`, `awk`, `sed`, etc.) to:
   - Find all lines containing both `[API]` and `ERROR`.
   - Extract the response time value in milliseconds (e.g., extracting `450` from `450ms` in the final column).
   - Calculate the mathematical average of these error response times.
   - Print *only* the average numeric value to standard output.
   Run your script against `/home/user/logs/api.log.1` and save the exact output to `/home/user/avg_error.txt`.

3. **Port Forwarding and Connectivity Diagnostics**:
   A local metrics server is already running and bound to port 8000. However, your observability dashboard is hardcoded to ping a healthcheck on port 9090. 
   Write a shell script at `/home/user/proxy.sh` containing a `socat` command that forwards local TCP port 9090 to local TCP port 8000. 
   Run this script in the background. 
   Finally, verify the connectivity by using `curl` to fetch `http://localhost:9090/health` and save the response body to `/home/user/health_check.txt`.