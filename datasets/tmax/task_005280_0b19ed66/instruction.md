You are a Site Reliability Engineer (SRE). We have a custom-built, high-performance health monitoring service written in C that sits behind an Nginx reverse proxy. Currently, the monitoring dashboard is down, and hitting the endpoint returns a 502 Bad Gateway error. 

Your investigation shows that Nginx and the backend C service are both trying to use Unix Domain Sockets (UDS), but there is a configuration mismatch and a bug in the service's HTTP response formatting. Furthermore, the service lacks an automated deployment script.

Your objectives are to fix the Nginx configuration, fix and enhance the C service, and write a shell script to manage their lifecycle.

**Step 1: Fix Nginx Configuration**
The Nginx configuration file is located at `/home/user/nginx/nginx.conf`. 
It is configured to run entirely in user space (listening on port 8080). 
Currently, it tries to proxy requests to `unix:/home/user/run/backend.sock`. However, the C service is hardcoded to listen on `/home/user/run/health_monitor.sock`.
Update `/home/user/nginx/nginx.conf` so the `proxy_pass` directive correctly points to the socket used by the C service.

**Step 2: Fix and Extend the C Service**
The C service source code is at `/home/user/src/monitor.c`.
1.  **Fix the HTTP Response:** The C program successfully accepts connections but Nginx drops the response because the C program sends `HTTP/1.1 200 OK\nSTATUS: UP` without the mandatory double carriage-return line-feed (`\r\n\r\n`) separating headers from the body. Fix the `write()` call in `monitor.c` to send a valid HTTP response: `HTTP/1.1 200 OK\r\n\r\nSTATUS: UP\n`.
2.  **Add Email Alert Logging:** Add logic in the request handler so that if the incoming request contains the string `GET /alert `, the service appends the exact line `ALERT: Service degraded` to the file `/home/user/mail/alerts.mbox` and responds with `HTTP/1.1 200 OK\r\n\r\nALERT SENT\n`.

**Step 3: Create the Lifecycle Management Script**
Write a shell script at `/home/user/deploy.sh` that performs the following actions in order:
1.  Compiles `/home/user/src/monitor.c` to an executable at `/home/user/bin/monitor`.
2.  Gracefully terminates any running instances of `monitor` and `nginx` (using `pkill` or similar; ignore errors if they aren't running).
3.  Cleans up any leftover socket file at `/home/user/run/health_monitor.sock`.
4.  Starts the compiled `/home/user/bin/monitor` in the background.
5.  Starts Nginx using the command: `nginx -c /home/user/nginx/nginx.conf -p /home/user/nginx/`
6.  Sleeps for 2 seconds to allow services to initialize.
7.  Runs `curl -s http://127.0.0.1:8080/` and saves the output to `/home/user/logs/health_check.log`.
8.  Runs `curl -s http://127.0.0.1:8080/alert` to trigger the mock email alert.

**Requirements & Constraints:**
- The script `/home/user/deploy.sh` must be executable (`chmod +x`).
- Do not change the Nginx port (8080).
- Do not run commands as root or use `sudo`. All processes must run as the `user` user.

Run `./deploy.sh` once you are done to ensure the system is up, the Nginx 502 error is resolved, the log file is generated, and the alert email file is populated.