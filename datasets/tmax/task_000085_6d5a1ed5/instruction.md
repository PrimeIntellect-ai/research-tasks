You are a release manager preparing a new deployment for our internal API infrastructure. The deployment consists of two services: a backend data service (written in Python) and a custom API gateway (written in C) that dynamically loads a shared library for request validation and rate limiting.

Currently, the multi-service environment in `/home/user/app/` is incomplete because the new rate-limiting shared library has not been implemented or integrated. Your task is to implement this library, ensure ABI compatibility with the gateway, write a unit test suite, and successfully bring up the integrated services.

Here are your specific requirements:

1. **Shared Library Implementation**:
   - Create a file `/home/user/app/plugin.c`.
   - Implement the C function with the exact ABI expected by the gateway: 
     `int process_request(const char* ip, const char* path);`
   - **Validation Rules**: Only paths that begin with `/api/v1/` are permitted. Any other path must be rejected (return `403`).
   - **Rate Limiting Rules**: For the path `/api/v1/data`, restrict requests to a maximum of **3 requests per IP address within any 2-second rolling window**. If the limit is exceeded, return `429`. (Assume a maximum of 10 unique IP addresses will be active at any time, so a simple in-memory structure is fine).
   - For all other valid requests, return `200`.
   - Compile this file into a shared library named `/home/user/app/libgateway_plugins.so`.

2. **Unit Testing**:
   - Create a C test program at `/home/user/app/test_plugin.c` that dynamically links to or includes your `plugin.c` logic.
   - The test program must invoke `process_request` to verify:
     - Rejection of invalid paths (e.g., `/api/v2/data`).
     - Acceptance of valid paths (e.g., `/api/v1/ping`).
     - Enforcement of the rate limit on `/api/v1/data` (the 4th request within 2 seconds from the same IP must fail).
   - Run the compiled test program and direct its output to `/home/user/test_results.log`. The log file must contain the string `ALL TESTS PASSED` upon success.

3. **Multi-Service Composition**:
   - The backend service script is located at `/home/user/app/backend.py` (listens on `127.0.0.1:8081`).
   - The gateway binary is located at `/home/user/app/gateway_bin` (listens on `127.0.0.1:8080`, proxies to `8081`). It expects `libgateway_plugins.so` to be present in its working directory.
   - Create a startup script `/home/user/app/start_services.sh` that launches both services in the background. 
   - Execute the startup script so the services are actively listening on their respective ports.

Make sure your C code handles time and state correctly for the rate limiter. Once you have compiled the shared library, run your unit tests, and started the services, you have completed your task. The automated verification system will test the active services via HTTP.