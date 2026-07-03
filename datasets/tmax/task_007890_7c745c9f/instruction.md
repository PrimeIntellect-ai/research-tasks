As a QA engineer, I need to dynamically stand up mock environments based on the version of a core system shared library we are testing. 

You must write a Python script at `/home/user/qa_agent.py` that acts as the test harness. 

The script must do the following:
1. Read the environment variable `TEST_LIB_PATH` to get the absolute path to a C shared library.
2. Load the shared library using Python's `ctypes`.
3. The library exposes a C function `const char* get_version()` which returns a semantic version string (e.g., "1.4.2" or "2.1.0"). You must properly define the ABI (return type) in `ctypes` to read this string.
4. Parse and compare this version string against the target version `"2.0.0"` using strict semantic versioning (you can use the `packaging.version` module).
5. Based on the semantic version comparison:
   - **If the version is strictly LESS THAN "2.0.0"**: 
     Start a basic REST API (using Python's built-in `http.server` or `wsgiref`) listening on `0.0.0.0` port `8080`.
     Any `GET` request to `/` should return a `200 OK` with the JSON payload: `{"status": "legacy", "version": "<the_version_string>"}`.
   - **If the version is GREATER THAN OR EQUAL TO "2.0.0"**:
     The shared library will additionally expose `int calculate_hash(int input_val)`. Ensure you map its ABI.
     Start a WebSocket server (using the `websockets` and `asyncio` libraries) listening on `0.0.0.0` port `8081`. 
     For every message received, parse it as an integer, pass it to `calculate_hash()`, and send back the resulting integer as a string.
6. **Immediately before starting the blocking server loop**, the script must write the port number it is about to listen on (either `8080` or `8081`) as plain text to `/home/user/active_port.txt`.

Ensure your script is executable and robust. We will test it by pointing `TEST_LIB_PATH` to different pre-compiled `.so` files and validating the respective API endpoints.