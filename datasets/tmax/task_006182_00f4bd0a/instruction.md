You are an infrastructure and security engineer tasked with setting up a custom Web Application Firewall (WAF) proxy system from scratch. You will need to write the build system, fix memory leaks, complete a state-machine parser in C++, and set up a reverse proxy.

Your workspace is in `/home/user/waf-proxy`.
Inside, you will find a partially implemented C++ program `waf.cpp`. This program listens on `127.0.0.1:9000` and parses incoming HTTP GET requests.

Perform the following tasks:

1. **State Machine & Parser Construction:**
   Open `/home/user/waf-proxy/waf.cpp`. The HTTP request parser implements a basic state machine. However, the `check_security` function is incomplete. Implement a state machine or simple substring search within this function to detect if the request URI contains the exact string `UNION SELECT`. If it does, return `false` (block the request, yielding a 403 response). Otherwise, return `true` (allow the request, yielding a 200 response).

2. **Memory Debugging:**
   The `waf.cpp` code contains a deliberate memory leak in the connection handling logic. Identify and fix this memory leak so that running the application handles requests without leaking memory (you can use Valgrind or AddressSanitizer to verify). 

3. **Polyglot / Conditional Build System:**
   Create a `CMakeLists.txt` file in `/home/user/waf-proxy`. It must:
   - Define an executable named `waf_server`.
   - Support two build configurations via conditional compilation:
     - If the CMake variable `ENABLE_ASAN` is set to `ON`, compile with AddressSanitizer (`-fsanitize=address -g`).
     - Otherwise, compile with standard release flags (`-O2`).
   - Create two build directories and build the project in both:
     - `/home/user/waf-proxy/build_debug` (configured with `-DENABLE_ASAN=ON`)
     - `/home/user/waf-proxy/build_release` (configured with `-DENABLE_ASAN=OFF`)

4. **Reverse Proxy Configuration:**
   Configure the local Nginx instance to act as a reverse proxy.
   - Create or modify an Nginx configuration file at `/home/user/nginx.conf`.
   - Nginx must listen on port `8080`.
   - Route all requests starting with `/api/` to the `waf_server` backend running on `127.0.0.1:9000`.
   - Start the Nginx service using your configuration file (e.g., `nginx -c /home/user/nginx.conf`).

5. **Execution & Logging:**
   Start the compiled release version of `waf_server` (`/home/user/waf-proxy/build_release/waf_server`) in the background.
   Using `curl`, send the following requests to the Nginx reverse proxy and append the HTTP status codes to `/home/user/test_results.log` (one status code per line):
   - `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/normal_request`
   - `curl -s -o /dev/null -w "%{http_code}" "http://localhost:8080/api/query?q=UNION%20SELECT"`

Ensure both `nginx` and `waf_server` are running when you finish.