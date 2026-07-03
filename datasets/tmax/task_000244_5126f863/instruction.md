You are tasked with resolving a service outage and implementing a basic security filter for our deployment pipeline.

We have a web application running on this machine. Nginx acts as a reverse proxy, but it is currently returning a "502 Bad Gateway" error when you attempt to access it. 

Here is the current state of the system:
- Nginx configuration is located at `/home/user/app/nginx.conf`.
- The backend service is running on `127.0.0.1:9090`.
- Nginx is configured to listen on port `8080`.

**Your objectives:**

1. **Fix the 502 Bad Gateway:** 
   Identify why Nginx cannot communicate with the backend service and fix the Nginx configuration. You will need to reload or restart the Nginx service (running locally via `/usr/sbin/nginx -c /home/user/app/nginx.conf -p /home/user/app/`) after making changes. When fixed, `curl -s http://127.0.0.1:8080/health` should return `OK`.

2. **Create a Request Sanitizer:**
   The recent service crashes were caused by directory traversal attacks. You must write a Bash script at `/home/user/waf.sh` that acts as a pre-filter. 
   - The script will take a single argument: the path to a text file containing an HTTP URI (e.g., `/api/v1/data` or `/api/v1/../../etc/passwd`).
   - If the URI contains any form of directory traversal (specifically `../` or its URL-encoded variants like `%2e%2e%2f`, `%2e%2e/`, `..%2f`), the script must print `REJECT` to stdout and exit with status code `1`.
   - If the URI is safe, the script must print `ACCEPT` to stdout and exit with status code `0`.
   - The script must use standard bash built-ins or coreutils.

Note: Our automated CI tests will verify your `waf.sh` against a hidden suite of safe and malicious URIs.