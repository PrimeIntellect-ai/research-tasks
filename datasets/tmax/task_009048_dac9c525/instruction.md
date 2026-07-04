You are tasked with fixing a broken web application configuration and writing an automated remediation script. 

The application uses an Nginx reverse proxy configuration located at `/home/user/app/nginx.conf`. Currently, requests are returning a 502 Bad Gateway error because the `proxy_pass` directive is pointing to an incorrect Unix socket path. The actual application backend is running and listening on a socket named `gunicorn.sock` located somewhere within the `/home/user/app/` directory tree.

Write a Bash script at `/home/user/fix_app.sh` that performs the following tasks. Ensure the script is executable.

1. **Idempotent Configuration Fix**: 
   The script must find the actual `gunicorn.sock` file inside `/home/user/app/` and update `/home/user/app/nginx.conf` to use this correct absolute path in the `proxy_pass` directive (replacing the incorrect socket path). The script must be idempotent (running it multiple times should not corrupt the file).

2. **Log Processing**:
   The Nginx error log is located at `/home/user/app/logs/error.log`. The script must parse this log file to find all connection errors, extract the unique Unix socket paths that Nginx attempted (and failed) to connect to, and save these paths to `/home/user/failed_sockets.txt`. 
   * The output file should contain only the absolute file paths (e.g., `/path/to/socket.sock`), one per line, sorted alphabetically. Do not include the `unix:` prefix or trailing colons.

3. **Firewall Rule Generation**:
   To expose the application, write a valid `iptables` command into a new file at `/home/user/port_forward.sh`. The command must forward incoming TCP traffic on port 80 on interface `eth0` to the local Nginx port `8080`.
   * Use the `REDIRECT` target in the `nat` table's `PREROUTING` chain.
   * Make sure `/home/user/port_forward.sh` is just a text file containing the exact `iptables` command on a single line. Do not execute the iptables command.

You do not need to restart Nginx; just create the script and run it once to fix the configuration and generate the required files.