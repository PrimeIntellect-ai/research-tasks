You are tasked with setting up a polyglot build and data processing pipeline. We need to integrate a high-performance Go library (which handles concurrent string manipulation) with a Python-based WebSocket server.

I have placed a Go source file at `/home/user/processor.go`. This file contains an exported C-compatible function `ProcessData(input *C.char) *C.char`. It processes a string using goroutines and channels, reversing and capitalizing each word.

Your objectives are:

1. **Build the Shared Library**:
   Write a bash script at `/home/user/build.sh` that compiles `/home/user/processor.go` into a C-shared library named `libprocessor.so` in `/home/user/`.

2. **Python ABI Management and WebSocket Server**:
   Write a Python script at `/home/user/server.py` that:
   - Uses `ctypes` to load `/home/user/libprocessor.so`.
   - Correctly defines the `argtypes` and `restype` for the `ProcessData` function to handle C-strings (ABI management).
   - Starts an asynchronous WebSocket server using the `websockets` library (you may need to install it) listening on `localhost` port `8765`.
   - When a client connects and sends a text message, the server must pass the string to the Go shared library's `ProcessData` function, and send the returned processed string back to the client.
   - The server must run continuously when executed.

3. **Integration Testing**:
   Write a Python test script at `/home/user/test_server.py` using `pytest` and `websockets` that:
   - Starts the `server.py` in a background process.
   - Connects to `ws://localhost:8765`.
   - Sends the exact string: `"polyglot concurrent pipeline"`
   - Receives the response and asserts that it equals `"TOLGYLOP TNERRUCNOC ENILEPIP"`
   - Closes the connection and terminates the server process.
   - Writes the literal string `"TEST PASSED"` to `/home/user/test_result.log` if the assertion succeeds.

Please ensure you install any necessary Python dependencies (e.g., `websockets`, `pytest`) in the user environment. 

Do not use root privileges. All files must be exactly at the specified paths.