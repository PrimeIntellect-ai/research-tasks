I need your help fixing our local development environment. Right now, our local Nginx reverse proxy is returning a "502 Bad Gateway" when accessing `http://127.0.0.1:8080/`.

Here is the setup:
- The Nginx configuration file is located at `/home/user/nginx/nginx.conf`.
- There is a Python backend API server located at `/home/user/app/backend.py`. 
- The backend is hardcoded to run on port 9000.
- Nginx does not require `sudo` to run, as it is configured to use unprivileged ports and local temporary directories inside `/home/user/nginx/`.

Your tasks:
1. Identify and fix the misconfiguration in `/home/user/nginx/nginx.conf` that is causing the 502 error.
2. The Python backend requires the environment variable `ENV_MODE` to be set to `production` to return a successful response; otherwise, it returns a 500 Internal Server Error. Ensure this is set when starting the backend.
3. Start the backend server and start Nginx in the background (using `nginx -c /home/user/nginx/nginx.conf`). Nginx is configured with `daemon off;`, so you may need to run it in the background or in a separate process.
4. Write a custom Python health check script at `/home/user/monitor.py`. This script must:
   - Make an HTTP GET request to `http://127.0.0.1:8080/`.
   - If the response status code is 200, write a single line to `/home/user/health.log` in the exact format: `HEALTHY: <JSON_RESPONSE_BODY>` (e.g., `HEALTHY: {"status": "healthy", "service": "backend"}`).
   - If the response is not 200, it should write nothing.
5. Run your `/home/user/monitor.py` script to generate the `/home/user/health.log` file so I can verify the system is fully operational.