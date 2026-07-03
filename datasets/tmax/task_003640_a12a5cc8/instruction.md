You are a system administrator tasked with fixing a broken web service setup. The local Nginx instance (listening on port 8080) is currently returning 502 Bad Gateway for its endpoints, and the upstream services are offline or misconfigured.

We have an architecture diagram located at `/app/architecture.png`. You will need to inspect this image (e.g., using OCR tools like `tesseract`) to determine the correct upstream destinations for our two backend services.

The services are:
1. **Python API**: Located in `/home/user/python_api/`. It uses Gunicorn to run a WSGI app.
2. **Node.js API**: Located in `/home/user/node_api/`. It's an Express application.

Current Issues:
- The Nginx configuration at `/home/user/nginx/nginx.conf` has incorrect upstream addresses. You must fix it using the routing information found in the `/app/architecture.png` diagram.
- The Python API needs to listen on a Unix socket, but the directory for it might not exist or lacks correct permissions.
- The Node.js API requires a specific environment variable to bind to the correct port matching Nginx's expectation.

Your tasks:
1. Read `/app/architecture.png` to find the correct routing paths:
   - What upstream address should the Nginx `location /python` block route to?
   - What upstream port should the Nginx `location /node` block route to?
2. Update `/home/user/nginx/nginx.conf` to reflect these correct upstreams.
3. Fix the environment, directory structure, and permissions so both apps can run securely and Nginx can communicate with them.
4. Create an automation script at `/home/user/deploy.sh` (make sure it is executable). When run, this script must:
   - Properly set up any needed directories or environment variables.
   - Start the Python API in the background.
   - Start the Node.js API in the background.
   - Start Nginx in the background (using your updated Nginx config).
5. Ensure your `deploy.sh` script executes successfully and all services stay running.

Verification:
We will run a benchmark script `/home/user/bench.py` that sends a barrage of requests to `http://127.0.0.1:8080/python` and `http://127.0.0.1:8080/node`. 
The verifier requires a numerical metric: the successful HTTP 200 response rate. 
You must achieve a success rate `>= 0.95` (95%).