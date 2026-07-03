You are tasked with organizing and fixing a partially migrated Python web project that relies on a vendored C library for secure URL path normalization. The previous developer left the project in a broken state due to a circular dependency in the build system and incomplete Python routing logic.

Your objectives:

1. **Fix and Build the Vendored C Library:**
   - A custom C library is located at `/app/fast-url-parser-1.2.0/`.
   - The `Makefile` has a build-preventing circular dependency error. Diagnose and fix the `Makefile`.
   - Compile the library by running `make` to produce the shared object `libfastparser.so`.
   - The C library exports a function with the signature: `void clean_path(const char* input, char* output)`. It strips directory traversal sequences (like `../`) from the input and writes to the `output` buffer (max 256 bytes).

2. **Implement the Python API Server:**
   - Write a standalone Python HTTP server at `/app/server.py` using only the standard library (`http.server` or `wsgiref`).
   - The server must listen on `127.0.0.1:8888`.
   - It must require an HTTP header: `Authorization: Bearer dev-sec-token`. Return HTTP 401 if missing or invalid.
   - Implement a single route: `GET /api/v1/normalize`.
   - The route must parse three query parameters: `path`, `min_version`, and `client_version`.
   - **Semantic Versioning Check:** Compare `client_version` and `min_version` using strict semantic versioning rules (major.minor.patch). If `client_version` is strictly lower than `min_version` or if either is malformed, return HTTP 403.
   - **Path Normalization:** If the version check passes, use Python's `ctypes` to load `/app/fast-url-parser-1.2.0/libfastparser.so` and pass the `path` parameter through the `clean_path` C function.
   - Return HTTP 200 with a JSON response in this exact format: `{"status": "success", "cleaned_path": "<result_from_c>"}`.

3. **Performance Benchmarking:**
   - Write a Python script `/app/bench.py` that makes 500 successful valid requests to your running server at `GET /api/v1/normalize?path=/var/../etc/passwd&min_version=1.0.0&client_version=1.2.0`.
   - Ensure the server handles these requests sequentially without crashing.
   - Measure the total time taken for the 500 requests and write the time in seconds (as a simple float) to `/app/bench_results.txt`.

Start the server in the background once completed. Do not use external libraries (like Flask or FastAPI) for the server.