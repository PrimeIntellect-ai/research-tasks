You are a script developer building a robust microservice utility for sorting and diffing large datasets. We need to deploy a C++ backend service behind an Nginx reverse proxy. The system is designed with a plugin architecture, so the core diffing logic must be compiled as a dynamically loaded shared library with a stable C ABI.

Your objective is to complete the system. You have been provided a workspace directory at `/home/user/workspace`.

Here are your specific tasks:

1. **Shared Library Implementation (ABI Management & Diffing)**
   Create a file `/home/user/workspace/plugin_diff.cpp`. It must expose a C-compatible function with the exact signature:
   `extern "C" void compute_diff(const char* list_a, const char* list_b, char* out_buf, size_t out_max_len);`
   - `list_a` and `list_b` are null-terminated strings containing comma-separated integers (e.g., "5,1,3").
   - The function must parse these strings, sort the integers, and compute the *symmetric difference* (elements present in one list but not the other).
   - The resulting integers must be formatted as a comma-separated string, sorted in ascending order, and written to `out_buf` (up to `out_max_len` bytes, including the null terminator).
   - Compile this file into a shared library named `libdiffplugin.so` in `/home/user/workspace`.

2. **C++ HTTP Backend Service**
   Write a C++ HTTP server in `/home/user/workspace/server.cpp`.
   - You must download and use the single-header `cpp-httplib` library (e.g., download `httplib.h` into your workspace).
   - The server must listen on `127.0.0.1:9090`.
   - It must dynamically load `libdiffplugin.so` at runtime (using `dlopen`/`dlsym`).
   - It must expose a `POST /internal/diff` endpoint. The request body will contain a JSON payload: `{"a": "5,1,3", "b": "3,2,4"}`.
   - The server should extract the strings, call the `compute_diff` plugin function (allocate an 8192-byte buffer for the output), and return the result as a plain text HTTP response (e.g., `1,2,4,5`).

3. **Nginx Reverse Proxy Configuration**
   Create a local Nginx configuration file at `/home/user/workspace/nginx.conf`.
   Since you do not have root access, configure Nginx to:
   - Run as the current user.
   - Use `/home/user/workspace/nginx_temp/` for all temporary files, logs, and pid files (you must create this directory).
   - Listen on `127.0.0.1:8080`.
   - Route all requests for `POST /api/diff` to the backend at `127.0.0.1:9090/internal/diff`.
   - Require an `Authorization` header exactly matching `Bearer super-secret-token`. If missing or invalid, return a 401 Unauthorized status.

4. **Startup**
   - Write a build script `/home/user/workspace/build.sh` that compiles `libdiffplugin.so` and `server.cpp`.
   - Write a start script `/home/user/workspace/start.sh` that launches the C++ backend in the background, and then starts Nginx using your custom config (e.g., `nginx -c /home/user/workspace/nginx.conf`).

Make sure your backend and proxy remain running after your setup is complete so they can be tested.