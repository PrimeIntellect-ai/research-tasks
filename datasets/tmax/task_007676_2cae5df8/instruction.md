You are an integration developer responsible for testing and securing a new WebSocket-based API gateway. The system consists of an Nginx reverse proxy, a Python WebSocket backend, and a high-performance C extension used for message parsing. 

Currently, the system is broken and insecure. You need to fix the C code, build the shared library, implement semantic version checking in the Python backend, configure the Nginx reverse proxy to support WebSockets, and write an integration test.

Here are your specific objectives:

1. **Fix and Build the C Extension:**
   In `/home/user/workspace/c_src/parser.c`, there is a C function `char* parse_message(const char* input)` that suffers from a buffer overflow vulnerability when handling large inputs. 
   - Fix the memory safety bug so it safely handles inputs of any size (returning a dynamically allocated string `"{PROCESSED: <input>}"`).
   - Write a Makefile or build command to compile this file into a shared library at `/home/user/workspace/lib/libparser.so`. Ensure it is compiled with `-fPIC -shared`.

2. **Implement Semantic Versioning in Backend:**
   The Python backend `/home/user/workspace/backend/server.py` uses the `websockets` library. 
   - Update `server.py` to inspect the `X-API-Version` HTTP header during the WebSocket handshake.
   - Accept the connection ONLY if the version is `>= 2.1.0` and `< 3.0.0` (using semantic versioning rules). Reject others with a 403 status.
   - Use the `ctypes` library in `server.py` to load `/home/user/workspace/lib/libparser.so` and pass incoming WebSocket messages through the C `parse_message` function. Send the returned string back to the client. Ensure memory allocated by the C function is freed if necessary (you may need to add a `free_message` function to your C code).

3. **Configure the Reverse Proxy:**
   Create an Nginx configuration at `/home/user/workspace/nginx/nginx.conf`.
   - It should listen on port 8080.
   - It must reverse-proxy all traffic to the Python backend running on `127.0.0.1:9000`.
   - It must be configured correctly to upgrade HTTP connections to WebSockets (passing the `Upgrade` and `Connection` headers).

4. **Write and Run the Integration Test:**
   Write a Python script at `/home/user/workspace/test_integration.py` that does the following:
   - Attempts to establish a WebSocket connection to `ws://127.0.0.1:8080` with header `X-API-Version: 1.9.9`. It should catch the rejection and log `VERSION_REJECTED` to `/home/user/workspace/integration_results.log`.
   - Attempts a connection with `X-API-Version: 2.5.0`.
   - Sends a payload of 500 'A' characters (which would have crashed the old C parser).
   - Receives the response, verifies it begins with `{PROCESSED: `, and logs `SUCCESS: <response>` to `/home/user/workspace/integration_results.log`.

Start the Nginx proxy (using your custom config) and the backend server in the background, then run your test script to generate the log file.