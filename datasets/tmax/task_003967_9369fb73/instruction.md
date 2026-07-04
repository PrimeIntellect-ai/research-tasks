You are tasked with fixing a security vulnerability in a polyglot web application (Python FastAPI with a C extension) and setting up a secure reverse proxy. 

A security patch was provided in `/home/user/security_fix.patch`, but it was generated against an older version of the codebase. Because the current codebase in `/home/user/app/` has been refactored (e.g., import order and formatting changes), the patch will fail to apply cleanly. 

Your objectives are:
1. **Patch Processing & Code Fix**: Examine `/home/user/security_fix.patch` and manually apply its intended security fixes (which prevent Server-Side Request Forgery - SSRF) to `/home/user/app/main.py`.
2. **API Construction**: Add a new REST endpoint to the FastAPI application in `main.py` at `GET /status` that returns a JSON response: `{"status": "secure"}`.
3. **Polyglot Build Orchestration**: Write a bash script at `/home/user/app/build.sh` that:
   - Installs the Python dependencies listed in `/home/user/app/requirements.txt`.
   - Compiles the C extension by running `python setup.py build_ext --inplace` inside the `/home/user/app/` directory.
   Make sure to execute this script so the C extension (`processor`) is built and available.
4. **Reverse Proxy Configuration**: Create an Nginx configuration file at `/home/user/nginx.conf`. It must:
   - Run as a daemon (or background process) and use `/home/user/nginx_error.log` for error logging. Ensure Nginx does not require root privileges (use high ports and `/tmp` for pid/run files if necessary).
   - Listen on port `8080`.
   - Proxy all requests to the FastAPI application running on `127.0.0.1:8000`.
   - Inject a custom HTTP response header: `X-Security-Protection: active` on all responses.
5. **Deployment**:
   - Start the FastAPI application on port `8000` (e.g., using `uvicorn main:app --port 8000 &`).
   - Start Nginx using your custom configuration.
   - Run a test request to your new endpoint via the proxy and save the raw JSON response of `curl -s http://127.0.0.1:8080/status` into `/home/user/test_result.txt`.

Ensure both services remain running in the background. The automated verification will test the Nginx proxy, the headers, the SSRF protection on the `/fetch` endpoint, and the `/status` endpoint.