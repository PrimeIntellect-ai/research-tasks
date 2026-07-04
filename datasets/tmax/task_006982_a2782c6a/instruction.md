You are acting as a Release Manager preparing a new deployment for our C++ backend service. The release candidate in `/home/user/release_prep` is currently failing to compile, fails its tests, and lacks the necessary proxy configuration for deployment.

Your goal is to fix the application, build it, pass the test suite, and run it behind a reverse proxy.

Here are your specific tasks:

1. **Apply Patch:** We received a patch file at `/home/user/release_prep/tests.patch` that updates the test fixtures. Apply this patch to the repository.
2. **Fix the Makefile:** The Makefile in `/home/user/release_prep/` is broken. It fails to link the test suite properly and is missing a library flag for threading (`-pthread`). Fix the Makefile so `make all` successfully builds both `api_server` and `run_tests`.
3. **Fix C++ Compilation & Serialization:**
   - The file `src/config_parser.cpp` contains a severe lifetime issue (returning a dangling reference) that prevents compilation or causes undefined behavior.
   - It also contains a bug in the JSON deserialization logic where it looks for the wrong key ("service_port" instead of "port").
   - Fix these issues so the application compiles safely and correctly parses the configuration.
4. **Run Tests:** Run `./run_tests`. Ensure it completes successfully. Redirect its standard output to `/home/user/test_results.log`.
5. **Configure Reverse Proxy:** 
   - Write an HAProxy configuration file at `/home/user/haproxy.cfg`.
   - The proxy must run completely in user-space (no root required).
   - It should listen on `127.0.0.1:8080`.
   - It must route all HTTP requests to our C++ `api_server` which will run on `127.0.0.1:9000`.
6. **Integration Verification:**
   - Start the C++ server in the background: `./api_server &`
   - Start HAProxy in the background: `haproxy -f /home/user/haproxy.cfg &`
   - Fetch the status of the service through the proxy: `curl -s http://127.0.0.1:8080/status`
   - Save the exact output of this curl command to `/home/user/deploy_ready.txt`.

Ensure all background processes are running when you consider the task complete. Automated verification will check the contents of `/home/user/test_results.log` and `/home/user/deploy_ready.txt`, as well as query the proxy directly.