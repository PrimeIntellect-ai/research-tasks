You are tasked with debugging and fixing a mixed C++/Python project located in `/home/user/ws_calc`. The project uses a C++ shared library for algorithmic computations, which is exposed to network clients via a Python asynchronous WebSocket server. 

Currently, the project is broken. The systems programmer who wrote it left two major issues:
1. An ABI and linking issue: The Python server uses `ctypes` to load the compiled C++ shared library, but it crashes on startup because it cannot find the expected C-exported function symbol, and the path to the library might not match the CMake output.
2. Missing tests: The system lacks integration tests to verify the WebSocket communication and data processing.

Your objectives:
1. **Fix the C++ ABI / Build Issue**: 
   - Modify `/home/user/ws_calc/src/libcalc.cpp` so that the `process_data` function is properly exported with C linkage, preventing C++ name mangling.
   - Build the shared library using CMake. Run your build process such that the resulting library is created at `/home/user/ws_calc/build/libcalc.so`.

2. **Fix the Python Server**:
   - Ensure `/home/user/ws_calc/server.py` successfully loads the shared library and maps the `process_data` function correctly.

3. **Write an Integration Test**:
   - Create a test file at `/home/user/ws_calc/tests/test_ws.py`.
   - Write a `pytest` suite using `pytest-asyncio` and `websockets` that tests the running `server.py`.
   - The test must connect to `ws://localhost:8765`, send a JSON message `{"op": "compute", "data": [1.5, 2.5, 3.5]}`, and assert that the received JSON response is exactly `{"result": [3.0, 5.0, 7.0]}` (since the C++ library multiplies inputs by 2.0).
   - Ensure your test handles the lifecycle of the WebSocket server (or assuming it runs in the background during the test).

4. **Generate Test Report**:
   - Run your test suite using `pytest` and output the results in JUnit XML format to `/home/user/ws_calc/test_results.xml`.

Ensure you install any necessary Python packages (like `websockets`, `pytest`, `pytest-asyncio`) using `pip` before running the tests.