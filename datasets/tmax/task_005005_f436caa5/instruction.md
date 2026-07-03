You are a mobile build engineer troubleshooting a broken CI pipeline.

In the CI environment, a lightweight local metrics API written in Python is failing to start. The application relies on a C shared library to parse raw build telemetry, but it crashes on startup due to an import ordering issue. Furthermore, the FFI binding to the C library was left incomplete by a previous engineer.

Your task is to fix the application and extract the telemetry data:

1. Navigate to `/home/user/build_pipeline/`.
2. Build the C shared library (`libtelemetry.so`) using the provided `Makefile`.
3. Fix the import order bug in `main.py`. Locally, the environment variable `PIPELINE_INIT` is set in the bash profile, so it passes. In CI, it is set by `config.py`. However, `main.py` imports the FFI wrapper before `config.py`, causing a crash.
4. Complete the implementation of `get_telemetry()` in `ffi_wrapper.py` using the `ctypes` module.
   - The C function signature is: `void process_telemetry(const char* input, char* output);`
   - You must call this function from Python, passing the byte string `b"BUILD_OK"` as the input, and provide a pre-allocated string buffer (size 256 is sufficient) for the output.
   - The C function will populate the output buffer with a serialized JSON string.
   - You must deserialize this JSON string into a Python dictionary and return it.
5. Start the REST API server by running `main.py` in the background (it binds to port 8000).
6. Perform a GET request to `http://127.0.0.1:8000/telemetry` using `curl`.
7. Save the raw JSON response to `/home/user/build_pipeline/final_output.json`.

Ensure the JSON file is correctly populated with the API response.