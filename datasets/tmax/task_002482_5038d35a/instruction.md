You are tasked with fixing a multi-file C++ project that acts as the backend for a Python-based web service. The project uses FFI (`ctypes`) to call a C++ shared library, but it currently fails to compile due to C-linkage and type errors. Additionally, the Python server wrapper has FFI configuration issues, and you need to set up a reverse proxy for testing.

The project is located in `/home/user/project` and contains the following files:
1. `processor.cpp`: A C++ file that parses a JSON array of objects (using a lightweight custom parser or standard string manipulation), sorts them by their `id` field, and returns the serialized JSON. It is intended to be called from Python, but it has a compilation error.
2. `Makefile`: Compiles `processor.cpp` into `libprocessor.so`.
3. `server.py`: A Python HTTP server that loads `libprocessor.so`, defines the FFI bindings, and serves POST requests on port 8080.

Your objectives:
1. **Fix Compilation**: Modify `/home/user/project/processor.cpp` so that it successfully compiles by running `make`. The function `sort_items` must have proper C-linkage (`extern "C"`), correctly accept a `const char*` JSON string, and return a dynamically allocated `const char*` (e.g., using `strdup`) so it can be safely read by Python.
2. **Fix FFI Bindings**: Edit `/home/user/project/server.py` to correctly configure the FFI boundary. Specifically, ensure the `restype` of the `sort_items` function is correctly set to `ctypes.c_char_p` so Python can read the returned string.
3. **Run the Server**: Start the fixed Python server (`python3 server.py &`) on port 8080.
4. **Configure Reverse Proxy**: Use a user-space tool like `socat` to create a reverse proxy listening on port 8000 that forwards all TCP traffic to `127.0.0.1:8080`. Run this in the background.
5. **Verify**: Write a bash script `/home/user/project/test_endpoint.sh` that uses `curl` to send the following JSON payload via a POST request to `http://127.0.0.1:8000`:
   `[{"id": 3, "val": "C"}, {"id": 1, "val": "A"}, {"id": 2, "val": "B"}]`
   The script must capture the response and save it exactly to `/home/user/project/final_output.json`.

Ensure all processes are running and the `final_output.json` file contains the correctly sorted JSON array.