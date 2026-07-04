You are tasked with migrating a legacy API validation and rate-limiting service to Go, orchestrating a polyglot build system, and writing an automated test suite.

Currently, we have a Python script that implements request validation and a simple rate limiter. We also have a highly optimized C library used for low-level IP blacklisting. You need to write a Go web server that integrates both the ported Python logic and the C library (via CGO), set up a Makefile to orchestrate the build of both languages, and write a Go test suite to verify the application.

Here is your environment setup:
- `/home/user/legacy/limiter.py`: Contains the reference Python implementation for request validation and rate limiting.
- `/home/user/c_src/filter.h` and `/home/user/c_src/filter.c`: Contains the C library with a function `int is_blocked(const char* ip);` which returns `1` if the IP is blocked, `0` otherwise.

Your objectives:
1. **Code Translation & API Implementation**: 
   Create a Go HTTP server in `/home/user/src/main.go`.
   - The server must listen on `127.0.0.1:8080`.
   - It should have a single endpoint: `POST /api/action`.
   - Port the validation and rate-limiting logic exactly as defined in `/home/user/legacy/limiter.py`.
   - Before applying the rate limit, the server must extract the client's IP address (from the `X-Forwarded-For` header, or default to `127.0.0.1` if missing) and pass it to the C function `is_blocked`. If `is_blocked` returns `1`, immediately return an HTTP `403 Forbidden` status code.
   - For invalid JSON or missing fields as defined in the Python script, return HTTP `400 Bad Request`.
   - If the rate limit is exceeded, return HTTP `429 Too Many Requests`.
   - Otherwise, return HTTP `200 OK`.

2. **Polyglot Build Orchestration**:
   Create a `/home/user/Makefile` with the following targets:
   - `lib`: Compiles the C code in `c_src/` into a shared library named `libfilter.so` in `/home/user/lib/`.
   - `build`: Depends on `lib`. Compiles the Go server into an executable located at `/home/user/bin/server`. You must configure CGO properly in the Makefile so it links against your newly built `libfilter.so`.
   - `clean`: Removes the `/home/user/bin/` and `/home/user/lib/` directories and their contents.
   *(Note: ensure the Go binary can find the shared library at runtime, e.g., using `-Wl,-rpath` or by assuming `LD_LIBRARY_PATH` will be set).*

3. **Testing**:
   Write an integration test in `/home/user/src/main_test.go` that:
   - Starts the server (or tests the HTTP handler directly using `httptest`).
   - Verifies the 400 Bad Request logic (invalid payload).
   - Verifies the 403 Forbidden logic (IP blacklisted by C library).
   - Verifies the 429 Too Many Requests logic (rate limit exceeded).
   - Verifies the 200 OK logic (successful request).
   
   Run your tests. If they pass, create an empty file at `/home/user/test_success.log` to indicate completion.

Make sure to create any missing directories (`/home/user/src`, `/home/user/bin`, `/home/user/lib`) either manually or inside your Makefile.