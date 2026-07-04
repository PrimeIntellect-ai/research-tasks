You are an engineer setting up an automated testing and polyglot build pipeline for a microservice. The service relies on a legacy configuration file, precise dependency versioning, and a reverse proxy for routing. You need to write the build and test scripts in Python to orchestrate this system.

All your work should be done in the `/home/user/project` directory. The directory already contains:
1. `versions.txt`: A list of available mock dependency versions for different libraries.
2. `legacy_config.b64`: A Base64-encoded file containing the legacy configuration in a simple `KEY=VALUE` format.
3. `backend.py`: A pre-written Python microservice that runs on `127.0.0.1:9090` and serves the contents of `config.json`.

Your task is to write a build and test pipeline consisting of two Python scripts:

**Part 1: `build.py`**
Write a Python script `/home/user/project/build.py` that does the following:
1. **Semantic Versioning:** Parse `versions.txt` to find all versions of `libA`. Calculate and select the *highest* semantic version of `libA` that satisfies the condition: `>= 1.1.0` and `< 2.0.0`. 
2. **Decoding and Translation:** Read `legacy_config.b64`, decode it from Base64 (which will yield UTF-8 strings of `KEY=VALUE` lines). Translate this data into a JSON dictionary and save it as `/home/user/project/config.json`.
3. **Reverse Proxy Configuration:** Generate a valid, user-space Nginx configuration file at `/home/user/project/nginx.conf`. Since you are not root, configure Nginx to run entirely out of `/home/user/project/` (using `/tmp/` or local directories for `pid`, `access_log`, and `error_log` if necessary, and turning off `daemon` or master processes as needed for testing). The Nginx server must:
   - Listen on `127.0.0.1:8080`.
   - Proxy all requests to `http://127.0.0.1:9090`.
   - Add a custom HTTP response header: `X-Library-Version` set exactly to the resolved semantic version of `libA` from Step 1.

**Part 2: `test_suite.py`**
Write a Python script `/home/user/project/test_suite.py` that verifies the built system:
1. Starts the `backend.py` process.
2. Starts the Nginx reverse proxy using your generated `nginx.conf`.
3. Makes an HTTP GET request to `http://127.0.0.1:8080/`.
4. Writes the test results to `/home/user/project/test_report.log` in exactly this format:
   ```
   STATUS: <HTTP_STATUS_CODE>
   HEADER: <VALUE_OF_X-Library-Version_HEADER>
   BODY: <RAW_JSON_RESPONSE_BODY>
   ```
5. Cleans up and terminates both processes.

You should execute `python build.py` and then `python test_suite.py` to ensure everything works and the `test_report.log` is generated successfully.