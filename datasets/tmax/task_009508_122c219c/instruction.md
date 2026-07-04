You are a QA engineer responsible for setting up a new automated testing environment for a high-performance Constraint Satisfaction problem solver. The development team has provided a C program that calculates the number of solutions to the N-Queens problem, but it is known to crash under certain conditions and consume excessive memory. 

Your objective is to fix the memory safety issues, run a memory profile, and expose the solver behind a reverse proxy for the QA integration tests.

Here is your detailed checklist:

1. **Fix Memory Safety and Undefined Behavior:**
   - The source code for the solver is located at `/home/user/app/solver.c`.
   - The program takes a single integer argument `N` (e.g., `./solver 8`) and prints the number of valid N-Queens configurations to `stdout`.
   - Debug and modify `/home/user/app/solver.c` to fix all memory leaks and buffer overflow issues.
   - Compile your fixed version to `/home/user/app/solver` using `gcc -O2 /home/user/app/solver.c -o /home/user/app/solver`.

2. **Memory Debugging and Profiling:**
   - Run the compiled solver through Valgrind to verify your fixes for `N=10`.
   - Save the complete Valgrind output (including the leak check summary) to `/home/user/valgrind.log`.
   - The log must demonstrate `0 errors from 0 contexts` and `All heap blocks were freed -- no leaks are possible`.

3. **Backend Service:**
   - A wrapper script is located at `/home/user/app/backend.py`. It listens on `127.0.0.1:8080` and exposes an endpoint at `/api/<N>`, which internally executes your `/home/user/app/solver` binary.
   - Start this backend script in the background.

4. **Reverse Proxy Configuration:**
   - Create an Nginx configuration file at `/home/user/nginx.conf`.
   - To run Nginx without root privileges, your config MUST include the following global directives at the top level or in the `http` block to avoid permission errors:
     ```nginx
     pid /tmp/nginx.pid;
     error_log /tmp/error.log;
     events {}
     http {
         access_log /tmp/access.log;
         client_body_temp_path /tmp/client_body;
         fastcgi_temp_path /tmp/fastcgi_temp;
         proxy_temp_path /tmp/proxy_temp;
         scgi_temp_path /tmp/scgi_temp;
         uwsgi_temp_path /tmp/uwsgi_temp;
         
         # YOUR SERVER BLOCK HERE
     }
     ```
   - Configure a `server` block to listen on port `8000`.
   - Set up a reverse proxy route such that requests to `http://127.0.0.1:8000/qa/<N>` are forwarded to `http://127.0.0.1:8080/api/<N>`. Note that the URI path must be rewritten/mapped correctly (e.g., `/qa/12` maps to `/api/12` on the backend).
   - Start nginx in the background using your custom configuration: `nginx -c /home/user/nginx.conf`.

5. **Verification:**
   - Execute an HTTP GET request to `http://127.0.0.1:8000/qa/12`.
   - Save the exact HTTP response body (which should just be the numeric solution) to `/home/user/response.txt`.