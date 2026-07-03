You are tasked with fixing a broken web architecture and implementing a basic shell-based security filter. 

We are running a custom, unprivileged setup with Nginx acting as a reverse proxy for a backend Python service. Nginx is listening on port `8080` and is configured via `/home/user/nginx/nginx.conf`. The Nginx service is currently returning a `502 Bad Gateway` error when accessing `http://127.0.0.1:8080/`.

Your objectives are:

1. **Fix the 502 Error**:
   Identify why Nginx cannot communicate with the backend service. The Nginx configuration is located at `/home/user/nginx/nginx.conf`. The backend service is known to be running reliably on `127.0.0.1:8081`. Update the configuration and reload the Nginx process so that `curl http://127.0.0.1:8080/` successfully returns the backend's response.

2. **Configure Log Rotation**:
   The Nginx logs in `/home/user/nginx/logs/` are growing out of control. Write a user-space logrotate configuration file at `/home/user/logrotate.conf`. It must rotate all `.log` files in that directory daily, keep exactly 7 rotated files, compress them, and ignore missing log files without error. 

3. **Write a Bash WAF (Web Application Firewall)**:
   We are experiencing malicious traffic. Write a robust Bash script at `/home/user/waf.sh` that takes exactly one argument (a log line string representing an HTTP request). 
   - The script must evaluate the input and exit with status code `0` (clean) or `1` (malicious).
   - A string is considered malicious if it contains any of the following patterns: `<script>`, `UNION SELECT`, or `../`.
   - The script must safely handle empty inputs, spaces, and unexpected characters without producing Bash syntax errors.

Ensure you do not require `sudo` for any of these steps. The Nginx process is running as the `user` account.