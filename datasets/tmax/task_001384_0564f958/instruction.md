You are stepping into a deployment scenario where a recent update broke the staging environment. 

A user-space `nginx` reverse proxy is currently returning a "502 Bad Gateway" when accessing the backend API. The API is a Python application managed by `supervisord` (running entirely in user space). Furthermore, the automated deployment script (`/home/user/deploy.sh`) seems to be failing to configure the environment variables correctly for the application.

Your task is to diagnose and fix the deployment so that the API successfully responds to requests.

System layout and initial state:
- Nginx configuration: `/home/user/nginx/nginx.conf`
- Nginx runs in user-space using `nginx -c /home/user/nginx/nginx.conf`
- Supervisord configuration: `/home/user/supervisor/supervisord.conf`
- Supervisord runs in user-space using `supervisord -c /home/user/supervisor/supervisord.conf`
- The backend application is located at `/home/user/app/server.py`. 
- The deployment script is at `/home/user/deploy.sh`.
- The main frontend proxy listens on `127.0.0.1:8080`. The API is mapped to the `/api/` path.

Requirements to resolve the issue:
1. Identify why Nginx is returning a 502 error for `http://127.0.0.1:8080/api/health` and fix the port mismatch between Nginx and the backend application. You can modify either Nginx or the backend configuration to align them on the same port.
2. The Python application crashes immediately upon startup. Inspect its code to determine what environment variable is missing. Update the process supervision configuration (`supervisord.conf`) to ensure this environment variable is passed to the application. The expected value for this environment variable is `staging_secret_99`.
3. Fix the `deploy.sh` script so that it correctly restarts the `supervisord` managed process after a deployment. Currently, it just exits. Update it so it contains the correct `supervisorctl` command to restart the backend API (the process name in supervisor is `backend-api`).
4. Apply your fixes, ensure both Nginx and Supervisord are running, and successfully curl the health endpoint.

Verification:
Once you have fixed the configurations and the services are running stably, run the following command and save its exact output to `/home/user/success.txt`:
`curl -s http://127.0.0.1:8080/api/health`

The automated test will verify the contents of `/home/user/success.txt`, the running state of the `backend-api` under supervisor, and the correctness of `deploy.sh`.