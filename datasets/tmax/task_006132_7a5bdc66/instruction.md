You are a QA engineer tasked with setting up a mock backend test environment to validate a legacy system's schema migration. 

The legacy backend uses a C shared library with a specific Application Binary Interface (ABI) to decode incoming telemetry payloads. You need to implement this shared library, set up a reverse proxy, and capture the output of a test request.

**Step 1: Implement the Shared Library**
Create a C source file at `/home/user/test_env/telemetry.c` and compile it into a shared library at `/home/user/test_env/libtelemetry.so`.
You must implement the following C function to maintain ABI compatibility with the mock server:

`int process_record(const char* hex_input, void* out_record);`

The `out_record` is a pointer to a custom data structure you must define in your C code according to this schema:
1.  A 32-bit unsigned integer `record_id` (little-endian).
2.  A 64-byte character array `decoded_text`.

**Data Encoding & Processing Rules:**
1.  The `hex_input` is a null-terminated string of hexadecimal characters (e.g., "01000000616263").
2.  Convert this hex string into raw binary bytes.
3.  The first 4 bytes of the raw binary data represent the `record_id` (in little-endian format).
4.  The remaining bytes represent the text data.
5.  Apply a ROT13 cipher to all alphabetical characters in the text data (leave non-alphabetical characters unchanged).
6.  Store the decoded string in the `decoded_text` field of `out_record`, ensuring it is null-terminated.
7.  Return `0` on success, or `-1` if the input is invalid.

**Step 2: Configure the Reverse Proxy**
We need to reverse-proxy traffic to our backend server. Create an HAProxy configuration file at `/home/user/test_env/haproxy.cfg`.
Configure HAProxy to:
- Listen on HTTP port `8080`.
- Forward all requests to a backend server running at `127.0.0.1:9000`.
Start HAProxy in the background using this configuration.

**Step 3: Start the Backend and Test**
A mock Python backend is already provided at `/home/user/test_env/server.py`. It listens on port `9000` and uses `ctypes` to call your `libtelemetry.so`.
1. Run the Python backend in the background.
2. Send a POST request to the HAProxy endpoint (port `8080`) with the following hex payload as the request body:
   `050000007572797962206a6265797121`
3. Save the exact HTTP response body received from HAProxy to `/home/user/test_env/result.json`.

Ensure all processes are running and the final `result.json` file is accurately populated.