You are tasked with fixing a broken web application deployment and setting up a basic Continuous Integration (CI) validation script. We have a local Python application that sits behind a user-space Nginx reverse proxy. Currently, hitting the proxy returns a "502 Bad Gateway" error, and static files are not serving correctly. 

Your objectives:

1. **Connectivity Diagnostics & Fixes**:
   The Nginx configuration file is located at `/home/user/nginx.conf` and the Python backend code is located at `/home/user/app/server.py`. Find the misconfiguration causing the 502 Bad Gateway error and fix it. Ensure both the Nginx proxy (listening on port 8080) and the backend are running successfully in the background. Note: you must run Nginx entirely in user-space without sudo.

2. **Link and Directory Structure Management**:
   The Nginx configuration relies on a document root at `/home/user/web_root/public` to serve files from the `/static/` URL path. Currently, this `public` path is a broken symlink. You need to repair the directory structure by making `/home/user/web_root/public` a valid symbolic link pointing to the actual static assets directory: `/home/user/app/static`.

3. **CI/CD Pipeline Construction**:
   Write a Python integration test script located at `/home/user/ci_pipeline.py` that validates the deployment. When executed, this script must:
   - Perform an HTTP GET request to `http://127.0.0.1:8080/` and assert it returns an HTTP 200 status code with the text "Backend is alive" in the body.
   - Perform an HTTP GET request to `http://127.0.0.1:8080/static/index.html` and assert it returns an HTTP 200 status code with the text "Hello from static" in the body.
   - Verify that `/home/user/web_root/public` is a valid symbolic link.
   - Output the test results to `/home/user/ci_report.json` in the exact following JSON format:
     ```json
     {
       "backend_ok": true,
       "static_ok": true,
       "symlink_valid": true
     }
     ```
     (If any test fails, the respective boolean should be `false`).

You must start both Nginx (using `nginx -c /home/user/nginx.conf`) and the Python backend in the background so that they are actively running. Run your CI pipeline script once to generate the `/home/user/ci_report.json` file.