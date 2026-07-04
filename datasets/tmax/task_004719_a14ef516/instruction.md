You are tasked with fixing and completing a polyglot build system and web backend for a new web security tool. The system uses a high-performance C library to compute custom secure checksums, wrapped by a Python web backend exposing both REST and WebSocket APIs. 

Currently, the project is completely broken. The build system fails to link/produce a loadable shared library, the C code crashes due to memory safety issues (undefined behavior), and the Python API and End-to-End tests haven't been implemented yet.

Your workspace is located at `/home/user/polyglot_auth`. It contains the following initial structure:
- `lib/secure_hash.c`: The C source file for the checksum library.
- `lib/secure_hash.h`: The C header file.
- `CMakeLists.txt`: The CMake build configuration.

Your tasks are to:

1. **Fix the Build System**:
   Modify `/home/user/polyglot_auth/CMakeLists.txt` so that it correctly compiles a *shared* library (`libsecure_hash.so`) instead of a static one, enabling Python's `ctypes` to load it dynamically. Build the project inside `/home/user/polyglot_auth/build`.

2. **Fix C Memory Safety Bugs**:
   Inspect and fix `/home/user/polyglot_auth/lib/secure_hash.c`. The function `compute_hash` suffers from an off-by-one buffer overflow resulting in memory corruption and undefined behavior when it writes the null terminator. Fix the memory allocation so it safely handles strings of any length.

3. **Implement the Python Backend**:
   Create a Python script at `/home/user/polyglot_auth/src/server.py` that:
   - Uses `ctypes` to load `/home/user/polyglot_auth/build/libsecure_hash.so`.
   - Starts a Flask REST API on port `5000`. It must have a route `POST /api/hash` that accepts a JSON payload `{"message": "<string>"}` and returns `{"hash": "<computed_hex_string>"}`.
   - Concurrently starts an asyncio WebSocket server on port `8765`. It should accept incoming text messages, compute the hash using the C library, and send back a JSON response: `{"hash": "<computed_hex_string>"}`.

4. **Orchestrate End-to-End Tests**:
   Write a Python test script at `/home/user/polyglot_auth/tests/test_e2e.py` that acts as a client. It must:
   - Send a `POST` request to `http://localhost:5000/api/hash` with `{"message": "HelloREST"}` and verify the hash returned.
   - Connect to `ws://localhost:8765`, send `"HelloWS"`, and verify the hash returned.
   - If both tests pass successfully, write the exact string `E2E_TESTS_PASSED` to `/home/user/polyglot_auth/test_results.log`. If they fail or crash, write `E2E_TESTS_FAILED`.

To complete the task:
- Ensure you install any necessary Python packages (like `Flask`, `websockets`, `requests`) via `pip`.
- Run your build system.
- Start `server.py` in the background.
- Run `test_e2e.py`.
- Ensure `/home/user/polyglot_auth/test_results.log` is generated with the success string.