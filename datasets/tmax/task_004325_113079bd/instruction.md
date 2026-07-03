You are a monitoring specialist tasked with fixing a broken local web service and setting up an automated reporting script.

Currently, there is a local Nginx instance configured to proxy requests to a backend service. However, it is returning 502 Bad Gateway errors because it is configured to forward traffic to the wrong Unix socket path.

Here is your objective:

1. **Fix the Nginx Configuration**:
   The Nginx configuration file is located at `/home/user/nginx/nginx.conf`. 
   Find the `upstream` block and correct the Unix socket path. The actual backend service creates its socket at `/home/user/app/backend.sock`. Update the configuration to point to this exact socket path.

2. **Create a Log Analysis Script**:
   Write a Bash script at `/home/user/alert_monitor.sh`. This script must:
   - Accept exactly one argument: the path to an Nginx error log file.
   - Use text processing tools (`grep`, `awk`, `sed`, etc.) to parse the file and find all upstream connection failure lines. These lines contain the strings `[error]`, `while connecting to upstream`, and `client:`.
   - Extract the Date, Time, Client IP, and the Upstream path from these lines.
   - Write the parsed results to a file located at `/home/user/502_report.txt`.
   
   The output in `/home/user/502_report.txt` MUST strictly follow this format for each matching line:
   `[YYYY/MM/DD HH:MM:SS] Client: <IP> - Upstream: <Upstream_Path>`
   
   *Example input line in the log:*
   `2023/10/25 14:32:01 [error] 1234#0: *1 connect() to unix:/home/user/app/wrong.sock failed (2: No such file or directory) while connecting to upstream, client: 192.168.1.10, server: localhost, request: "GET / HTTP/1.1", upstream: "http://unix:/home/user/app/wrong.sock:/", host: "localhost"`
   
   *Expected output line in `/home/user/502_report.txt`:*
   `[2023/10/25 14:32:01] Client: 192.168.1.10 - Upstream: http://unix:/home/user/app/wrong.sock:/`

Make sure your script `/home/user/alert_monitor.sh` has executable permissions. We will test it by passing an existing error log file `/home/user/nginx/logs/error.log` to it.