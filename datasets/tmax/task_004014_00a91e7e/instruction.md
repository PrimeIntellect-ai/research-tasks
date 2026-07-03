You are tasked with fixing a broken web service and hardening its reliability by implementing a process supervisor in Bash.

Currently, there is a local Nginx instance configured to run on port 8080. It is supposed to serve requests by proxying them to a backend service communicating over a Unix domain socket. However, curling `http://localhost:8080` currently returns a 502 Bad Gateway error because Nginx is configured with the wrong upstream socket path. 

The backend service is located at `/home/user/backend.py` and creates a socket at `/home/user/run/app.sock`. Nginx is mistakenly looking for `/home/user/run/backend.sock`.

Your tasks:
1. Fix the Nginx configuration file located at `/home/user/nginx/nginx.conf` so it points to the correct upstream Unix domain socket.
2. The backend script `/home/user/backend.py` is currently not running, and it is prone to crashing. Write a Bash script at `/home/user/supervise.sh` that acts as a process supervisor. 
    - The script must start `/home/user/backend.py`.
    - It must monitor the backend process. If the backend process exits or crashes, the supervisor must automatically restart it.
    - Every time the supervisor restarts the backend (excluding the initial start), it must append the exact line `[CRASH] restarted backend` to the log file `/home/user/supervise.log`.
3. Start your supervisor script (`/home/user/supervise.sh`) in the background.
4. Start Nginx in the background using the fixed configuration file: `nginx -c /home/user/nginx/nginx.conf`.

Verify your setup by ensuring `curl -s http://localhost:8080` returns the backend's success message, and that if you manually kill the backend process, your supervisor revives it and logs the event.