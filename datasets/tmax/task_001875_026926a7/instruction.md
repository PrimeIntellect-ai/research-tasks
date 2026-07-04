You are a web developer working on a high-performance, secure data retrieval pipeline. The system consists of an Nginx reverse proxy, a Python Flask API, and a legacy C-based validation microservice. Currently, the pipeline is incomplete, fails to compile, and is severely unoptimized.

Your goal is to fix, complete, and optimize the system so it can handle a high-throughput load securely.

System Architecture:
- Nginx: Listens on port 8080 and proxies requests starting with `/api/` to the Flask app.
- Flask App (Service): Runs on port 5000. Located in `/app/flask_app/`.
- C Backend (Service): Runs on port 9000. Located in `/app/c_backend/`.
- Startup: The script `/app/start_services.sh` launches all three.

Tasks to complete:
1. **C Program Repair & Optimization**:
   The C backend in `/app/c_backend/` has a broken `Makefile` (fails to compile). Fix the syntax errors in the Makefile. Additionally, the `validator.c` code contains a severe artificial performance bottleneck (an unoptimized prime-checking loop used for delays). Fix the Makefile to compile successfully with the `-O3` flag, and modify the C code to remove the artificial delay bottleneck so the service responds instantly.

2. **Code Translation**:
   In `/app/flask_app/legacy_crypto.js`, there is a legacy signature validation function. You must translate this exact logic into Python and save it as `validate_signature` in `/app/flask_app/crypto_utils.py`. The algorithm processes a resource ID and a secret to generate an expected signature.

3. **URL Routing and Integration**:
   Update the Flask application in `/app/flask_app/app.py`. 
   - Add a new route: `GET /api/v1/resource/<resource_id>`.
   - It must extract a `sig` parameter from the query string.
   - Use your translated Python function to validate the `sig` against the `resource_id` (the server secret is "SUPER_SECRET_KEY").
   - If the signature is invalid, return a 403 HTTP status.
   - If valid, establish a TCP connection to the C backend on `localhost:9000`, send the `resource_id` (as a newline-terminated string), read the response, and return it to the user as a JSON object: `{"data": "<response_from_c>"}`.

4. **Service Orchestration**:
   Ensure `/app/start_services.sh` properly starts Nginx, Flask (e.g., using gunicorn or python app.py), and the compiled C backend. All services must run concurrently and seamlessly handle requests flowing from Nginx -> Flask -> C Backend.

When you are finished, start the services using `/app/start_services.sh` and ensure they are running in the background. Leave the system in this ready state.