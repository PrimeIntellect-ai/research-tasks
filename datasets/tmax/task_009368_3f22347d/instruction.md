You are an engineer tasked with porting an algorithmic backend component to a minimal, containerized microservices environment. You need to write the core logic in C, expose it via a Python server using FFI, and route traffic to it via a reverse proxy running in user space.

Here are the requirements:

1. **Algorithmic C Core (`/home/user/workspace/src/mergediff.c`)**
   Write a C file that implements the following function:
   `void compute_diff(const int* a, int len_a, const int* b, int len_b, int* out_only_a, int* len_only_a, int* out_only_b, int* len_only_b, int* out_both, int* len_both);`
   
   The function takes two strictly sorted arrays of integers (`a` and `b`, with no duplicates) and their lengths. It must populate the pre-allocated output arrays with:
   - Elements only in `a` (`out_only_a`), and set `*len_only_a`
   - Elements only in `b` (`out_only_b`), and set `*len_only_b`
   - Elements present in both (`out_both`), and set `*len_both`
   
   **Conditional Build Requirement:** When the macro `MINIMAL_BUILD` is defined, the C code must compile cleanly without including `<stdio.h>` or `<stdlib.h>`. Compile this into a shared library at `/home/user/workspace/libmergediff.so` using:
   `gcc -shared -fPIC -DMINIMAL_BUILD -O2 /home/user/workspace/src/mergediff.c -o /home/user/workspace/libmergediff.so`

2. **Python FFI Server (`/home/user/workspace/server.py`)**
   Create a Python 3 script using the standard `http.server` library (do not use Flask/FastAPI) that listens on `127.0.0.1:5000`. 
   - Use the `ctypes` library to load `/home/user/workspace/libmergediff.so`.
   - Implement a POST endpoint at `/diff` that accepts a JSON payload: `{"a": [1, 5, 10], "b": [5, 10, 15]}`.
   - The arrays `a` and `b` will always be sorted integers.
   - Allocate the appropriate `ctypes` arrays, call `compute_diff`, and return a JSON response with HTTP status 200: `{"only_a": [1], "only_b": [15], "both": [5, 10]}`.

3. **Reverse Proxy Configuration (`/home/user/workspace/nginx.conf`)**
   Create a user-space Nginx configuration file that runs a reverse proxy listening on `127.0.0.1:8080` and proxies requests for `/diff` to `127.0.0.1:5000`.
   Since you are not root, your `nginx.conf` must use `/tmp` for the `pid` file, `client_body_temp_path`, `proxy_temp_path`, `fastcgi_temp_path`, `uwsgi_temp_path`, and `scgi_temp_path`. It must run in the foreground (or allow the tests to start it easily). Set `error_log` and `access_log` to `/dev/null` to save space.

4. **Execution**
   - Start the Python server in the background: `python3 /home/user/workspace/server.py &`
   - Start Nginx in the background: `nginx -c /home/user/workspace/nginx.conf &`
   - Write a log file `/home/user/workspace/status.log` containing exactly the word `READY` when all services are up.

Ensure everything is configured and running properly. We will test the functionality via `curl` against port 8080.