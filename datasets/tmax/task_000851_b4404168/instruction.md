You are a release manager preparing an integration test environment for a new deployment. We have a test suite that passes in local mock environments but fails in CI. The issue stems from two missing pieces in the CI environment: our reverse proxy routing is unconfigured, and our mock C backend incorrectly evaluates semantic versions.

The environment is located in `/home/user/deployment_test/`.

Here is what you need to do:

1. **Fix the Semantic Versioning in the Backend**
   Inspect `/home/user/deployment_test/backend.c`. It runs a simple HTTP mock server on port 9090. The function `check_version` currently uses a naive `strcmp` to compare semantic versions. The backend requires a minimum API version of `2.2.0`. Because of the naive string comparison, requests with version `2.10.0` are being incorrectly rejected as being older than `2.2.0` (since `"2.10.0" < "2.2.0"` in ASCII).
   Rewrite the `check_version` function in `backend.c` to properly parse and compare semantic versions (Major.Minor.Patch as integers).
   Recompile the backend: `gcc -o backend backend.c`

2. **Configure the Reverse Proxy**
   Create an Nginx configuration file at `/home/user/deployment_test/nginx.conf`.
   The configuration must:
   - Run in the foreground (or background) but NOT require root (use `/tmp/` for pids/logs if needed).
   - Listen on port `8080`.
   - Implement URL routing: Intercept requests to `/api/<version>/<endpoint>` (e.g., `/api/2.10.0/deploy`).
   - Proxy these requests to the C backend at `http://127.0.0.1:9090/<endpoint>`.
   - Extract the `<version>` from the URL and pass it to the backend using the HTTP header `X-API-Version`.

3. **Run and Verify**
   - Start the compiled `./backend` program in the background.
   - Start Nginx using your configuration: `nginx -c /home/user/deployment_test/nginx.conf` (run it in the background).
   - Execute the provided test script: `bash /home/user/deployment_test/test.sh > /home/user/deployment_test/results.log`

Ensure that the final output in `/home/user/deployment_test/results.log` contains the correct HTTP status codes for all test cases.