You are an integration developer working on a hybrid C/Python telemetry system. We are transitioning our telemetry audio decoding pipeline to a Python-based WebSocket service, but the core decoding logic remains in a legacy C library.

Your task is to build and integrate this system:

1. **Shared Library Management**: 
   There is a C source file located at `/app/libtelemetry.c`. Compile this file into a shared library named `libtelemetry.so`. The library contains three functions:
   - `void init_decoder();`
   - `char* decode_audio(const char* filepath);`
   - `void free_string(char* str);`

2. **FFI & Initialization**:
   Write a Python wrapper using `ctypes` to interface with `libtelemetry.so`. 
   *Crucial state requirement*: You must call `init_decoder()` strictly *before* attempting to decode. Failing to do so, or importing certain heavy Python network modules before the C library initializes its internal buffers, has been known to cause segfaults in CI (the classic import ordering bug). Ensure your wrapper initializes the library immediately upon load.
   Ensure you properly define the C-types (ABI) for arguments and return types. You must free the memory returned by `decode_audio` using `free_string` to avoid memory leaks.

3. **Data Processing**:
   We have received a new audio artifact located at `/app/telemetry.wav`. Use your Python FFI wrapper to pass this file path to `decode_audio`. 
   The C function will return a hex-encoded string. You must decode this hex string into standard ASCII/UTF-8.

4. **WebSocket Integration**:
   Create and start an asynchronous WebSocket server in Python (e.g., using the `websockets` library) listening strictly on `127.0.0.1` port `8765`.
   When a client connects and sends the exact text message `"GET_TELEMETRY"`, the server must respond with the decoded ASCII string derived from `/app/telemetry.wav`. 
   For any other message, it should respond with `"INVALID_COMMAND"`.

Keep the server running in the foreground so it can be tested by our automated verification suite.