You are acting as a systems programmer. We have a workspace in `/home/user/workspace` containing a C file `libcompute.c`, a broken Python web server `app.py`, and a broken Nginx configuration `nginx.conf`. 

Your goal is to fix the issues, build the shared library, run the services, and verify the pipeline.

1. **Shared Library Build:**
   Compile `libcompute.c` into a shared library named `libcompute.so` in `/home/user/workspace`. Ensure it's compiled with position-independent code (`-fPIC`).

2. **Fix the Python Application (`app.py`):**
   The application acts as an HTTP server on `127.0.0.1:8080`. It receives JSON POST requests on the `/process` endpoint. The JSON is a list of objects, e.g., `[{"id": 1, "value": 10.5}, {"id": 2, "value": -3.2}]`.
   
   The Python app needs to serialize this JSON into a specific binary format and pass it to the `process_records` function in `libcompute.so`.
   
   *Serialization format:* For each record, pack the `id` as an unsigned 16-bit integer (little-endian) and `value` as a 32-bit float (little-endian). Concatenate them. (6 bytes per record).
   
   *ABI Management:* `app.py` currently attempts to load `libcompute.so` and call `process_records`. However, the `ctypes` bindings are incorrect, leading to wrong return values or crashes.
   The C function signature is:
   `double process_records(const unsigned char* data, int length);`
   Where `length` is the total number of bytes in `data`. Fix `app.py` to correctly define `argtypes` and `restype` for this function.

   When the Python server processes the request, it should return a plain text response containing the double value returned by `process_records` formatted to 4 decimal places.

3. **Reverse Proxy Configuration:**
   Fix the provided `nginx.conf`. It should run as a reverse proxy listening on `127.0.0.1:8000`. Any request sent to `/api/process` should be proxied to the Python server at `127.0.0.1:8080/process`. 
   Ensure Nginx runs in the foreground or as a local user daemon without requiring root privileges. The configuration should be suitable for running `nginx -c /home/user/workspace/nginx.conf -p /home/user/workspace/nginx_prefix/`.

4. **Testing and Logging:**
   Start the Python server and Nginx in the background. 
   Then, use `curl` to send the following JSON payload to the Nginx endpoint `http://127.0.0.1:8000/api/process`:
   `[{"id": 10, "value": 1.5}, {"id": 20, "value": 2.5}]`
   
   Save the exact HTTP response body received from curl into `/home/user/workspace/result.log`.