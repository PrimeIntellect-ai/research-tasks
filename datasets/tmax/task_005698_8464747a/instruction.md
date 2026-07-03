You are an integration developer responsible for testing a high-performance mathematical API. 

We have a fast C implementation of a statistical variance algorithm located at `/home/user/workspace/math_ext.c` and a partially finished Python WebSocket server that uses it in `/home/user/workspace/server.py`.

Your task is to fix the application and write an end-to-end integration test:

1. **Build the C library**: Compile `/home/user/workspace/math_ext.c` into a shared library named `libmath.so` in the same directory.
2. **Fix the Server**: Edit `/home/user/workspace/server.py` to properly load `libmath.so` and configure the FFI `argtypes` and `restype` for the `calculate_variance` C function using Python's `ctypes`.
3. **Write an E2E Test**: Write a Python script at `/home/user/workspace/test_integration.py`. This script should:
   - Connect to the running WebSocket server at `ws://localhost:8080`.
   - Send the following JSON payload: `{"op": "variance", "data": [10.5, 15.2, 12.8, 9.1, 14.4]}`
   - Receive the response payload.
   - Save the exact received JSON string to `/home/user/workspace/integration_output.json`.

To complete the task, you should start the server in the background, run your integration test, and ensure `integration_output.json` contains the correct result.

Make sure your server uses the correct data types. The C function signature is:
`double calculate_variance(double* data, int length);`