You are acting as a systems programmer responsible for setting up a Python-based web service that relies on a custom C library for Web Application Firewall (WAF) request validation. The project is located in `/home/user/workspace`. 

Currently, the C library cannot be built due to a linking issue in the Makefile, and there is a known vulnerability in the WAF logic that needs to be patched before deployment. Additionally, the Python server wrapper needs to be written with rate-limiting capabilities.

Perform the following tasks:

1. **Dependency Management:**
   Create a Python virtual environment at `/home/user/venv`. Activate it, install `Flask`, and generate a `/home/user/workspace/requirements.txt` file containing the frozen dependencies.

2. **Patch Processing:**
   You will find a patch file at `/home/user/workspace/waf_security.patch` and the C source at `/home/user/workspace/waf.c`. Apply the patch to `waf.c` to fix the missing request validation logic.

3. **Makefile Repair and C Compilation:**
   The `Makefile` in `/home/user/workspace` is broken. It attempts to build a standard executable instead of a shared library and is missing the appropriate compiler flags (`-fPIC`, `-shared`). Fix the `Makefile` and run `make` so that it successfully compiles `waf.c` into a shared library named `/home/user/workspace/libwaf.so`.

4. **Web Server Implementation:**
   Write a Flask application in `/home/user/workspace/server.py` that does the following:
   - Runs on `0.0.0.0` at port `8080`.
   - Exposes a `POST /submit` endpoint that reads the raw request body as a string.
   - **Rate Limiting:** Implement an in-memory rate limiter restricting each client IP address to a maximum of 3 requests per rolling 10-second window. If a client exceeds this, immediately return a `429 Too Many Requests` HTTP status.
   - **Request Validation:** Use Python's `ctypes` module to load `/home/user/workspace/libwaf.so`. The library exposes a function `int validate_request(const char* payload)`. Pass the raw request body to this function. 
   - If `validate_request` returns `0`, the request is malicious. Return a `403 Forbidden` HTTP status and append a line to `/home/user/workspace/waf.log` in the exact format: `[<CLIENT_IP>] REJECTED: <payload>`.
   - If `validate_request` returns `1`, the request is safe. Return a `200 OK` HTTP status with the text `Success`.

5. **Execution:**
   Start your Flask server in the background so it is ready to accept requests, and write its Process ID (PID) to `/home/user/workspace/server.pid`.