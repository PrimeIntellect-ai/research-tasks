You are a mobile build engineer maintaining the local CI pipeline simulator. We have a multi-service architecture located in `/home/user/app/` that routes build requests based on semantic version constraints. 

Currently, the setup is incomplete. You need to configure the reverse proxy, implement the expression evaluation logic in Python, and ensure the services communicate correctly.

Here is what you need to do:

1. **Reverse Proxy Setup (`/home/user/app/nginx.conf`)**:
   Configure Nginx to run as a reverse proxy listening on `127.0.0.1:8080` (without requiring root, so store pids and logs in `/home/user/app/nginx/`).
   - Requests to `/build` should be proxied to the Python router service at `127.0.0.1:8000`.
   - Requests to `/status` should be proxied to the Go builder service at `127.0.0.1:8001`.

2. **Python Router Implementation (`/home/user/app/router.py`)**:
   Create a Python HTTP server (you can use Flask or the standard `http.server`) listening on `127.0.0.1:8000`.
   - It should accept POST requests at `/build`.
   - The JSON payload will look like: `{"version": "2.1.0-beta", "constraint": ">= 2.0.0", "target": "android"}`.
   - You must parse and evaluate the semantic version constraint. (You may use standard libraries or `packaging.version`).
   - If the `version` satisfies the `constraint`, the Python service must concurrently forward the `target` as a POST request to `http://127.0.0.1:8001/trigger` with payload `{"target": "<target>"}` and return its JSON response with HTTP status 200.
   - If it fails the constraint, return HTTP 400 with JSON `{"error": "version constraint not met"}`.

3. **Service Startup (`/home/user/app/start.sh`)**:
   Write a bash script `start.sh` that starts Nginx using your config, starts the Python router in the background, and starts the pre-compiled Go builder binary located at `/home/user/app/builder`.

Make sure all services are running. We will test the entire flow by sending HTTP POST requests to the Nginx proxy on port 8080.