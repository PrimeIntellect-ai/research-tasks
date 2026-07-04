You are a script developer tasked with creating a fast data processing microservice. You need to fix a provided C library, compile it, and write an HTTP server in the language of your choice that uses this library via Foreign Function Interface (FFI) to process incoming requests.

Here are your instructions:

1. **Fix and Compile the C Library**
   In `/home/user/fast_process/`, there is a C file `fast_hash.c` and a `Makefile`. The Makefile is currently broken and does not correctly produce a shared library (`.so` file). Fix the `Makefile` so that running `make` successfully compiles `fast_hash.c` into a shared library named `libfasthash.so`.

2. **Create the Processing API**
   Write an HTTP server script in `/home/user/server/` (you can use Python, Node.js, Ruby, or any language you prefer; install any packages you need). The server must run on `0.0.0.0` at port `8080`.

   The server must expose a single endpoint: `POST /process`
   - It expects a JSON payload: `{"payload": "<string>"}`
   
   **Validation Rules:**
   - If the JSON is malformed, the `payload` key is missing, or the value is not a string, return an HTTP 400 Bad Request.
   - The `payload` string MUST be strictly alphanumeric (only A-Z, a-z, and 0-9). If it contains any other characters, return an HTTP 400 Bad Request.

   **Rate Limiting Rules:**
   - The endpoint must allow a maximum of 5 requests per second globally.
   - If a 6th request is received within a 1-second rolling window, return an HTTP 429 Too Many Requests.

   **Processing (FFI):**
   - If the request is valid and within the rate limit, the server must use FFI (e.g., `ctypes` in Python, `ffi-napi` in Node) to load `/home/user/fast_process/libfasthash.so`.
   - Call the C function `int compute_hash(const char* input)` with the `payload` string.
   - Return an HTTP 200 OK with the JSON response: `{"hash": <integer_result>}`.

3. **Deployment**
   Start your server in the background so it is listening on port 8080.
   Once the server is fully running and ready to accept requests, create a file named `/home/user/server_ready.txt` with the exact word `READY`. 

Do not write any background daemon managers; simply starting the process in the background (`&`) is sufficient. Ensure your API strictly adheres to the status codes and validation rules.