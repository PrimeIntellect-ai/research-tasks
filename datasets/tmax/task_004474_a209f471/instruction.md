You are helping a team migrate an old Python 2 system to a modern microservices architecture. Previously, a Python 2 script used `ctypes` to call a custom C library that solved a constraint satisfaction problem (0/1 Knapsack). To allow the new Python 3 services to use this solver without dealing with C ABIs directly, you need to expose this C library via a Go REST API. However, the legacy C code has a memory safety bug that caused sporadic crashes, which you must fix first.

Here are your instructions:

1. **Fix the C Code & Compile the Shared Library:**
   You will find the legacy C code at `/home/user/legacy/solver.c` and its header at `/home/user/legacy/solver.h`. 
   The function `int solve_knapsack(int* weights, int* values, int n, int capacity)` contains a memory safety vulnerability (buffer overflow) because it uses a fixed-size stack array for its dynamic programming table, but `capacity` can now be larger than the hardcoded size. 
   - Fix the memory safety bug in `solver.c` (ensure it handles `capacity` up to 1000 without crashing or leaking memory).
   - Compile it into a shared library named `libsolver.so` in the `/home/user/legacy/` directory.

2. **Create the Go API Server:**
   Write a Go web server in `/home/user/api/server.go` that wraps this shared library using `cgo`.
   The server must listen on `127.0.0.1:8080`.
   
   **Endpoint:** `POST /solve`
   **Request JSON Format:**
   ```json
   {
     "items": [
       {"weight": 10, "value": 60},
       {"weight": 20, "value": 100}
     ],
     "capacity": 50
   }
   ```
   
   **Requirements:**
   - **Deserialization & Serialization:** Parse the incoming JSON, extract the arrays of weights and values, and pass them to the C function. Return the result as JSON: `{"max_value": <int>}`.
   - **Request Validation:** Return a `400 Bad Request` HTTP status if `capacity` is missing, less than 1, or greater than 1000. Return `400` if `items` is empty or has more than 100 elements.
   - **Rate Limiting:** Implement a global rate limit. The API must not accept more than 5 requests per second. If this limit is exceeded, return a `429 Too Many Requests` HTTP status.
   - **Shared Library Linking:** Ensure your Go program is properly configured to link against `/home/user/legacy/libsolver.so` at runtime.

3. **Execution:**
   Write a shell script at `/home/user/api/start.sh` that builds the Go application, ensures the shared library is findable by the linker (e.g., via `LD_LIBRARY_PATH`), and runs the server in the background. The script must write the server's PID to `/home/user/api/server.pid`.

Ensure your server runs correctly and implements all requirements.