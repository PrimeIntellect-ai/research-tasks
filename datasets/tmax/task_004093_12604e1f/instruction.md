You are a system administrator tasked with fixing a broken web service deployment. 

Currently, an Nginx instance is configured to serve a Python-based web application on `127.0.0.1:8080`, but requests to `http://127.0.0.1:8080/health` are returning a "502 Bad Gateway" error. 

The application architecture has the following components:
1. **Nginx:** The Nginx configuration is located at `/home/user/nginx/nginx.conf`. It is supposed to proxy traffic to a local Unix domain socket at `/home/user/app/backend.sock`. Nginx is run as the current user using this specific config.
2. **Backend Application:** The backend is a Python script located at `/home/user/app/server.py`. However, it has a legacy interactive security measure: when executed, it prompts `Enter startup key: ` on standard output. It requires the exact string `DeployKey2023!` to be entered before it will start and bind to the socket.

Your objective is to fix the deployment and completely automate the startup and verification process. 

Please complete the following steps:
1. **Fix the Nginx Configuration**: Locate and correct the Nginx configuration file (`/home/user/nginx/nginx.conf`) so it correctly points to the intended Unix socket (`/home/user/app/backend.sock`).
2. **Automate the Backend Startup**: Write an `expect` script named `/home/user/start_backend.exp`. This script must spawn the `/home/user/app/server.py` process, wait for the `Enter startup key: ` prompt, send the correct key (`DeployKey2023!`), and allow the backend process to continue running in the background. 
3. **Write a Robust Deployment Script**: Write a Python script at `/home/user/deploy.py` that acts as the deployment lifecycle manager. This script must:
    - Execute your `start_backend.exp` script to launch the backend.
    - Start (or restart) the Nginx daemon using the command: `nginx -c /home/user/nginx/nginx.conf -p /home/user/nginx`
    - Robustly poll `http://127.0.0.1:8080/health` (implementing a retry mechanism with backoff) until it receives a successful HTTP 200 response with the text `OK`.
    - Once successful, the script must write the exact string `DEPLOYMENT_SUCCESS: 200 OK` to a log file at `/home/user/deploy_status.log`.
    - If the backend fails to start or Nginx continues to return 502 after multiple retries, gracefully handle the error and exit.

**Verification criteria:**
- `/home/user/nginx/nginx.conf` must have the correct upstream socket path.
- `/home/user/start_backend.exp` must correctly automate the interactive prompt.
- Running `python3 /home/user/deploy.py` must result in a functioning Nginx server on port 8080 and the creation of `/home/user/deploy_status.log` containing `DEPLOYMENT_SUCCESS: 200 OK`. 

You can assume `nginx`, `expect`, and `python3` are installed. You have standard user privileges.