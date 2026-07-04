You are tasked with fixing a web application setup that is currently returning a 502 Bad Gateway error. 

An Nginx reverse proxy is configured to run entirely in user space. Its configuration file is located at `/home/user/nginx.conf`. It listens on port 8080 and is supposed to proxy requests to a backend Python service.
The backend application is located at `/home/user/app/server.py`. 

Currently, if you try to access `http://127.0.0.1:8080`, it fails. Your objectives are:

1. Identify why the Nginx proxy is returning a 502 error and fix the configuration in `/home/user/nginx.conf`. The backend service expects to run on port 8081.
2. The Nginx process might not be running or needs to be reloaded. Ensure Nginx is running using the configuration at `/home/user/nginx.conf`.
3. The backend service frequently crashes in production, so you need to create a simple process supervision bash script at `/home/user/app/monitor.sh`. 
   - This script must be executable.
   - It should check if the Python backend is running (e.g., by checking if port 8081 is open or checking the process list).
   - If the backend is not running, the script must start `/home/user/app/server.py` in the background, redirecting its standard output and standard error to `/home/user/app/server.log`.
   - The script must be idempotent (if the backend is already running, it should do nothing).
4. Run your `monitor.sh` script to start the backend.
5. Once everything is working, perform an HTTP GET request to `http://127.0.0.1:8080/` and save the exact output to `/home/user/success.txt`.

Constraints:
- You do not have root access. All commands must be run as the standard `user`.
- Do not modify `server.py`.
- Use standard bash commands for your script.