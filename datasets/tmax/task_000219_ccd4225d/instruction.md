You are a system administrator tasked with fixing a broken web service stack. The system is running entirely in user space in your home directory `/home/user`.

Currently, requests to the Nginx reverse proxy on port 8080 return a "502 Bad Gateway" error. The backend service is an interactive script that listens on a port, but it frequently crashes and requires a passphrase to start. 

Your objectives are to fix the Nginx configuration, automate the backend's startup, ensure it stays alive, and set up a port forward.

Here are the details and your tasks:

1. **Fix Nginx Configuration:**
   The configuration file is located at `/home/user/nginx.conf`. It is currently configured to reverse proxy traffic to the wrong backend port. Find the correct port (by analyzing the backend script) and fix the Nginx configuration. Reload or start Nginx using:
   `nginx -c /home/user/nginx.conf -p /home/user/`

2. **Automate the Backend Startup (`expect` scripting):**
   The backend service is located at `/home/user/backend.sh`. When executed, it interactively prompts: `Enter passphrase to unlock server: `. The passphrase is `admin_secret_99`.
   Write an `expect` script at `/home/user/start_backend.exp` that spawns `/home/user/backend.sh`, waits for the exact prompt, sends the correct passphrase, and hands over control or keeps the process running.

3. **Process Supervision (`bash` scripting):**
   The backend service is unstable and will exit after handling a few requests. Write a Bash supervisor script at `/home/user/supervisor.sh` that runs the `expect` script in an infinite loop. If the `expect` script exits, the supervisor should immediately restart it. Start this supervisor in the background.

4. **Port Forwarding:**
   Use `socat` to forward TCP traffic from local port 9000 to the Nginx port (8080). Run this in the background.

5. **Verification:**
   Once everything is running (Nginx, the supervisor keeping the backend alive, and the socat forwarder), make 5 sequential HTTP GET requests using `curl` to `http://127.0.0.1:9000`. 
   Append the raw output of each `curl` command to a log file at `/home/user/verification.log`.

Make sure your supervisor and port forwarder are running in the background before you run the curl tests. The backend service will respond with "OK_BACKEND_ACTIVE".