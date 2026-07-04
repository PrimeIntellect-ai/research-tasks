You are an expert systems programmer and backend developer. We are migrating an old data processing system to a new Python-based REST API, but we are running into issues with some legacy compiled components.

You have been provided with the following files in the `/app` directory:
1. `/app/oracle_parser` - A stripped, compiled binary executable. It takes a raw URL path and query string as a command-line argument and outputs a strictly formatted JSON string representing parsed constraints. 
2. `/app/libsolver.so` - A compiled C shared library containing our core constraint satisfaction engine.
3. `/app/api_template.py` - A skeleton Python script that attempts to load `libsolver.so` via `ctypes` and set up an HTTP server.

Your objectives:

1. **Fix the Linking Issue:** 
   The `libsolver.so` library currently fails to load due to a missing dependency. If you inspect it, you will see it requires `libhelpers.so.1`. We managed to find the file `libhelpers.so.1` in `/app/legacy_libs/`, but `libsolver.so` doesn't know where to find it. You must configure the environment or patch the binaries so that `libsolver.so` can be loaded successfully by Python.

2. **Implement the REST API:**
   Modify `api_template.py` (or write a new Python script at `/home/user/api.py`) to run an HTTP web server listening exactly on `127.0.0.1:8080`. 
   
   The server must handle `GET /solve?...` requests. 
   When a request is received:
   - Pass the raw request path and query string (e.g., `/solve?target=100&w=10,20,30`) to the `/app/oracle_parser` binary via a subprocess.
   - Parse the JSON output from the binary, which will look like `{"target": 100, "weights": [10, 20, 30]}`.
   - Use Python's `ctypes` to call the `int run_solver(int target, int* weights, int num_weights)` function from the loaded `libsolver.so`. You will need to correctly configure the `argtypes` and `restype` in Python.
   - Return an HTTP 200 response with a JSON payload in the format: `{"status": "success", "result": <integer_result>}`.

3. **Start the Service:**
   Leave the Python API server running in the background listening on `127.0.0.1:8080`. Output the PID to `/home/user/server.pid`.

Ensure your Python server correctly handles HTTP protocol responses (including headers and content-type).