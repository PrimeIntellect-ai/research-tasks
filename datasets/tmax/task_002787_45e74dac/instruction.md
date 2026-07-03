I am dealing with a broken local staging environment and I need your help to fix it. We have a Python-based backend API behind an unprivileged Nginx reverse proxy. Currently, any request to the Nginx server returns a 502 Bad Gateway error. 

Here is what you need to know about the environment:
1. **Nginx:** 
   - Config file: `/home/user/nginx/nginx.conf`
   - Nginx is currently running and listening on `127.0.0.1:8080`.
   - It is configured to proxy requests to our backend on `127.0.0.1:9000`.
   - Nginx is running entirely in user-space (unprivileged).

2. **Python Backend:**
   - Source directory: `/home/user/app/`
   - Entry point: `/home/user/app/server.py`
   - The backend is currently NOT running because it crashes on startup. 
   - It expects its application data to be available at `/home/user/app/mnt/data.json`.
   - The actual data is stored on a separate volume at `/home/user/storage/data.json`. 

3. **Staged Deployment:**
   - We use a simple staged deployment structure. The active release should always run from `/home/user/deploy/current/`.

Your tasks are:
1. **Fix the Storage "Mount":** You cannot use the `mount` command without root access. Instead, simulate the mount by creating a symbolic link at `/home/user/app/mnt` that points to `/home/user/storage` so the application can find `data.json`.
2. **Fix and Deploy the Backend:**
   - Diagnose why `server.py` might be failing or misconfigured (it currently has a bug regarding the port it binds to).
   - Fix the Python script so it properly listens on `127.0.0.1:9000`.
   - Perform a deployment by copying the fixed `/home/user/app/` directory contents into `/home/user/deploy/current/`. (Create the directory structure if it does not exist).
   - Start the backend server from the `/home/user/deploy/current/` directory in the background.
3. **Connectivity & Nginx:**
   - Verify Nginx can now talk to the backend. If the Nginx config has any routing mistakes pointing to the wrong port, fix them and reload Nginx using `nginx -c /home/user/nginx/nginx.conf -s reload`.
4. **Verification:**
   - Make an HTTP GET request to Nginx at `http://127.0.0.1:8080/api/status`.
   - Save the raw HTTP response body to `/home/user/success.log`.

Do not use sudo or root privileges. Ensure the final backend process is running in the background and Nginx successfully proxies the request, yielding an HTTP 200 response in your log file.