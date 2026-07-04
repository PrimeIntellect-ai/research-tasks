You are a platform engineer maintaining a CI/CD pipeline for a hybrid microservice. The service consists of a C++ core backend compiled as a shared library (`libbackend.so`), which is called by a Python lightweight web server (`server.py`) using FFI (`ctypes`). 

Recently, the integration tests started failing due to out-of-memory errors on long-running instances. We suspect a memory leak in the C++ library.

Your task:
1. **Fix the Memory Leak**: Analyze and fix the memory leak in `/home/user/app/libbackend.cpp`. The current code allocates memory dynamically for every request but the Python wrapper does not free it. Fix the C++ code so that it no longer leaks memory (e.g., by using a static buffer or standard C++ practices that do not require changing the Python `ctypes` bindings, as you are not allowed to modify `server.py`).
2. **Compile the Library**: Compile the fixed C++ code into a shared library at `/home/user/app/libbackend.so` using `g++` (ensure it is compiled with `-fPIC -shared`).
3. **Configure a Reverse Proxy**: The CI/CD environment requires the service to be accessed via port 8000, but the Python server runs on port 9000. Use `socat` to set up a background reverse proxy that listens on TCP port 8000 and forwards requests to `localhost:9000`.
4. **Run Memory Profiling**: Start the python server using `valgrind` to verify your fix. Run the server in the background: `valgrind --leak-check=full python3 /home/user/app/server.py > /home/user/app/server.log 2> /home/user/app/valgrind_fixed.log &`.
5. **Execute Integration Test**: While the server and proxy are running, use `curl` to send exactly 5 HTTP GET requests to `http://localhost:8000/`.
6. **Generate the Report**: Gracefully terminate the Python server (using `kill -TERM`) so Valgrind finishes and writes the memory summary to `/home/user/app/valgrind_fixed.log`. 

The automated test will verify:
- `libbackend.so` is successfully compiled with your fix.
- A `socat` process is running and proxying port 8000 to 9000.
- `/home/user/app/valgrind_fixed.log` exists and contains `definitely lost: 0 bytes`.