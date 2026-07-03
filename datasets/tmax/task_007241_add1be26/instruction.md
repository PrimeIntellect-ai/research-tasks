Our local staging environment is currently broken. Our Nginx reverse proxy is returning a 502 Bad Gateway when accessing the backend application, and Nginx itself might be failing to start properly due to missing TLS certificates.

Your objective is to diagnose and fix the Nginx configuration, ensure TLS is properly set up, write an Expect script for testing connectivity to our local mail relay, and start the services. 

Here are the details and requirements:

1. **Fix Nginx Configuration:**
   - The Nginx configuration file is located at `/home/user/nginx/nginx.conf`.
   - It is supposed to act as a reverse proxy (HTTPS on port 8443) to our backend Python application.
   - Currently, requests to `https://127.0.0.1:8443/status` return a 502 Bad Gateway.
   - Investigate the backend app located at `/home/user/app/server.py` to find out what port it actually listens on, and update the Nginx configuration to proxy to the correct port.

2. **Web Server TLS Setup:**
   - The `nginx.conf` expects a certificate and key at `/home/user/nginx/certs/server.crt` and `/home/user/nginx/certs/server.key`.
   - These files are missing. Generate a self-signed X.509 certificate (and unencrypted RSA key) valid for 365 days and place them in the specified paths. (Create the directory if it does not exist).

3. **Expect Script for SMTP Diagnostics:**
   - The Python backend relies on a local SMTP server on port 2525.
   - Write an Expect script at `/home/user/test_smtp.exp` that tests this connectivity.
   - The script must:
     - Spawn a `nc` (netcat) or `telnet` connection to `127.0.0.1 2525`.
     - Expect a string containing `220`.
     - Send the command `HELO localhost\r`.
     - Expect a string containing `250`.
     - Send the command `QUIT\r`.
     - Expect a string containing `221`.

4. **Service Startup and Verification:**
   - Write a bash script at `/home/user/start_all.sh` that starts the Python backend app (`python3 /home/user/app/server.py`) and Nginx (`nginx -c /home/user/nginx/nginx.conf`) in the background. Make sure the script exits cleanly while leaving the services running.
   - Execute your `start_all.sh` script.
   - Verify that Nginx is proxying correctly by running `curl -s -k -o /dev/null -w "%{http_code}" https://127.0.0.1:8443/status`. 
   - Write the exact HTTP status code returned by the `curl` command to a file named `/home/user/result.log`.

Note: You do not need root access to run Nginx with this specific configuration, as it binds to port 8443 and uses local directories for its PID and logs.