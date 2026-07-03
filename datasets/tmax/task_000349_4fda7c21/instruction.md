You are an internal site administrator responsible for modernizing the user account management portal. Our old records were archived, and we need to deploy a new highly-available service. 

Your task is to set up a reverse-proxied Python backend, managed by a process supervisor, that exposes user data securely.

Here are the requirements:

1. **Extract Authorization Token:**
   There is a scanned image of an old infrastructure config file located at `/app/archived_record.png`. Use OCR (e.g., `tesseract`, which is preinstalled) to extract the text. You will find a line containing the text `ADMIN_TOKEN: <token>`. You must use this exact `<token>` to secure your new backend.

2. **Implement the Python Backend (`/home/user/backend.py`):**
   Write a Python HTTP server (you can use `http.server` or `Flask`, which is installed). The script must accept two command-line arguments: the port to listen on, and the admin token.
   It must listen on `127.0.0.1` at the provided port and implement two endpoints:
   - `GET /status`: Returns an HTTP 200 response with JSON `{"status": "ok"}`.
   - `GET /users`: Checks for the presence of the `X-Admin-Token` HTTP header. 
     - If the header matches the token extracted from the image, return HTTP 200 with JSON `{"users": ["alice", "bob", "charlie"]}`.
     - If the header is missing or incorrect, return HTTP 401 Unauthorized.
   - Additionally, every response (from both endpoints) MUST include an HTTP header `X-Backend-Port` containing the port number the backend instance is running on.

3. **Configure the Reverse Proxy (`/home/user/nginx.conf`):**
   We need to load balance the traffic. Configure `nginx` to run as an unprivileged user.
   - It must listen on `127.0.0.1:8080`.
   - It must load balance incoming requests evenly (round-robin) across two instances of your backend running on `127.0.0.1:9001` and `127.0.0.1:9002`.
   - Configure Nginx to log access logs to `/home/user/proxy_access.log` and error logs to `/home/user/proxy_error.log`.
   - Make sure Nginx runs in the foreground (`daemon off;`) so it can be supervised properly. Do not use default pid locations that require root; place the pid file at `/home/user/nginx.pid`.

4. **Process Supervision (`/home/user/supervisord.conf`):**
   Create a configuration file for `supervisord`. It must define and manage three processes:
   - `backend1`: Your python script running on port 9001.
   - `backend2`: Your python script running on port 9002.
   - `proxy`: The nginx reverse proxy using your configuration file.
   Ensure all log files and pid files for supervisord itself are written to `/home/user/`.

5. **Start the System:**
   Start `supervisord` using your configuration file in the background (e.g., `supervisord -c /home/user/supervisord.conf`). Ensure that all three processes reach the `RUNNING` state.

Do not use sudo or root permissions, as you are running as the unprivileged `user`. 
Once you have started supervisord and verified the endpoints are accessible via port 8080, you have completed the task.