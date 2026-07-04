You are a web developer building a real-time risk streaming feature. The core pricing algorithm is written in C for performance, but it needs to be exposed via a Python WebSocket server that also calculates a rolling numerical metric (Simple Moving Average). You also need to write a robust test suite that mocks the C library.

Your workspace is `/home/user/workspace`. 
Inside it, there is a C file named `pricing.c` containing a single function:
`double compute_risk(double value, double volatility, double time_to_maturity);`

Your tasks are to:

1. **Shared Library Build:**
   Compile `/home/user/workspace/pricing.c` into a shared library named `/home/user/workspace/libpricing.so`. Ensure it is compiled correctly as position-independent code.

2. **WebSocket Server & Numerical Algorithm:**
   Create a Python script `/home/user/workspace/server.py`. 
   - It must run a WebSocket server on `ws://localhost:8765` using the `websockets` and `asyncio` libraries.
   - Use `ctypes` to load `libpricing.so` and properly define the ABI (argtypes and restype as C `double`).
   - For every incoming WebSocket message (expected to be a JSON string like `{"value": 100.0, "volatility": 0.2, "time": 1.5}`), the server must calculate the risk using the C function.
   - The server must also compute a Simple Moving Average (SMA) of the last 3 computed risk values *for the current connection*. If fewer than 3 values have been calculated for the connection, the SMA is the average of the available values.
   - The server should respond with JSON: `{"risk": <computed_risk>, "sma_3": <computed_sma>}`.

3. **Test Fixtures and Mocking:**
   Create a test file `/home/user/workspace/test_server.py` using `pytest`.
   - Write a test fixture that uses `unittest.mock.patch` to mock the loaded C library's `compute_risk` function so that it always returns exactly `10.0`, ensuring tests don't depend on the actual C binary.
   - Write an asynchronous test function `test_websocket_stream` that connects to your server (or tests the handler directly), sends three messages, and verifies that the `sma_3` output in the third response is `10.0`.
   
4. **Execution & Documentation:**
   - Write a shell script `/home/user/workspace/run_all.sh` that installs dependencies (`websockets`, `pytest`, `pytest-asyncio`), compiles the C library, and runs `pytest test_server.py > /home/user/workspace/test_report.log`.

Make sure your server can handle multiple sequential requests on the same connection. Do not start the server in a blocking way at the end of `server.py` if it prevents tests from importing it; ideally, encapsulate the server startup in an `if __name__ == "__main__":` block.