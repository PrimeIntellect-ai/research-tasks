You are a platform engineer optimizing a mathematical service used in our CI/CD pipelines to calculate prime metrics. 

Your task is to write a high-performance C++ module, bind it to a Python web server, and update our database schema.

1. **C++ Library**:
   Create a C++ file at `/home/user/math_lib.cpp`. Implement a function that calculates the nth prime number. 
   The function must have the signature `int nth_prime(int n)` and be exported with `extern "C"` so it can be called from Python. (Note: the 1st prime is 2, the 2nd is 3, etc.).
   Compile this file into a shared library at `/home/user/libmath.so`.

2. **Schema Migration**:
   There is an existing SQLite database at `/home/user/metrics.db`. It contains a table named `calculations` with the following schema:
   `id INTEGER PRIMARY KEY, n INTEGER, result INTEGER`
   Perform a schema migration on this database to add a new column named `timestamp` of type `DATETIME` with a default value of `CURRENT_TIMESTAMP`. 

3. **Python Server**:
   Create a Flask web server at `/home/user/server.py` (you may need to install Flask via pip).
   The server must:
   - Use `ctypes` to load `/home/user/libmath.so` and configure the FFI to call `nth_prime`.
   - Implement a GET route `/prime/<int:n>`.
   - When the route is called, it should invoke the C++ function to get the nth prime.
   - Insert a new record into the `calculations` table in `/home/user/metrics.db` with the `n` and the computed `result`.
   - Return a JSON response in the exact format: `{"n": n, "result": result}`.

4. **Execution**:
   Start the Flask server in the background so it listens on `0.0.0.0:8080`.
   Write the Process ID (PID) of the running server to `/home/user/server.pid`.
   Leave the server running.