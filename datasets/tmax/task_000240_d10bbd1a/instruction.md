I need help migrating and upgrading an old Python 2 financial analysis service to Python 3. The current service is terribly slow and uses outdated protocols. 

Here is the current state of the system in the `/app` directory:
- `/app/legacy/math_ops.py`: A Python 2 script containing a naive implementation of a Rolling Window Median algorithm.
- `/app/legacy/server.py`: An old Python 2 HTTP polling server.

You need to architect and implement a modern, high-performance replacement in Python 3.

**Requirements:**

1. **C FFI Implementation (`/app/math_lib.c` and `/app/libmath.so`)**
   - Write a highly optimized C function to compute the rolling median.
   - Signature: `void rolling_median(const double* input, int length, int window_size, double* output)`
   - Compile this to a shared library at `/app/libmath.so`.

2. **WebSocket Server (`/app/ws_server.py`)**
   - Write a Python 3 WebSocket server (e.g., using the `websockets` or `fastapi` library) listening on `0.0.0.0:8080`.
   - The server must accept connections and listen for JSON messages formatted as: `{"action": "compute", "window": int, "data": [float, ...]}`.
   - Use `ctypes` to invoke your compiled C library to perform the computation.
   - Return the result as JSON: `{"result": [float, ...]}`. For the first `window - 1` elements, the output should be `0.0`.

3. **Request Validation and Rate Limiting**
   - A local Redis server is already running on `127.0.0.1:6379`.
   - Implement rate limiting: a single IP address must not exceed 10 requests per second.
   - If a client exceeds this, the server must immediately close the WebSocket connection with close code `4000`.

Please write the C code, compile it, and write and start the Python 3 server. Leave the server running in the background. My automated benchmark will connect to `ws://127.0.0.1:8080` to evaluate both the correctness (Mean Squared Error) and the performance (Execution Speed) of your implementation.