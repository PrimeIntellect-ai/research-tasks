We have an Nginx server running locally on port 8080 serving as a reverse proxy. However, requests to the `/api` endpoint are currently failing with a "502 Bad Gateway" error. 

Your tasks are as follows:
1. We have an architecture diagram located at `/app/arch_diagram.png`. This image contains the documentation for the correct backend port that Nginx should be proxying to. Read this image to find the correct port number.
2. The backend service is running on a restricted local network environment. You must write an idempotent Python script at `/home/user/setup_tunnel.py` that establishes a local port forward to this backend service (simulate this by forwarding a local port to a mock backend running on port 8000 via an SSH tunnel to `localhost`).
3. Update the Nginx configuration file located at `/home/user/nginx/nginx.conf` (which is included in the main Nginx process) to point the `/api` proxy pass to the tunneled port you discovered from the image. Reload Nginx without restarting it to apply the changes.
4. We need to verify the fix with a load test. Write a Python script at `/home/user/load_test.py` that sends 100 concurrent HTTP GET requests to `http://localhost:8080/api`. The script must output a single floating-point number representing the success rate (number of 200 OK responses divided by total requests, e.g., `1.0` for 100%).

Ensure your setup scripts are idempotent and could be safely integrated into a CI/CD pipeline. Nginx is configured to run under the current user, so no root privileges are needed.