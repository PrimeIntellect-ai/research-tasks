You are a build engineer managing legacy artifacts. We have a core numerical calculation module written in C that we need to expose as an internal microservice, but its build system is broken and the configuration parameters were lost, existing only in a scanned schematic.

Your task consists of three parts:

1. **Information Recovery:**
   There is an image containing the system configuration located at `/app/calibration.png`. 
   Use OCR (the `tesseract` package is preinstalled) to extract the text from this image. You need to identify two values from the scan:
   - `ACCESS_TOKEN`: The authentication token required for the API.
   - `BASE_MULTIPLIER`: A floating-point coefficient used in the numerical algorithm.

2. **C Build System Repair:**
   In the `/app/legacy_calc` directory, you will find `matrix_ops.c`, `matrix_ops.h`, and a `Makefile`. 
   The `Makefile` is broken (incorrect syntax, missing flags for shared library generation, etc.). 
   Fix the `Makefile` and compile the code to produce a shared object file named `libmatrix_ops.so` in the same directory. The C code exports a function: `double compute_calibrated(double input, double coeff);`.

3. **Python FFI and API Integration:**
   Write a Python HTTP server in `/home/user/server.py`. The server must:
   - Listen on exactly `127.0.0.1:8000`.
   - Accept `POST` requests at the `/process` endpoint.
   - Expect a JSON payload in the format: `{"value": <float>}`.
   - Require authentication via an HTTP header: `Authorization: Bearer <ACCESS_TOKEN>` (using the token recovered from the image). If the token is missing or invalid, return a 401 status code.
   - If authenticated, use Python's `ctypes` module to load `/app/legacy_calc/libmatrix_ops.so`.
   - Call the `compute_calibrated` C function, passing the `value` from the JSON payload as the first argument, and the `BASE_MULTIPLIER` (recovered from the image) as the second argument.
   - Return a JSON response with status 200 in the format: `{"status": "ok", "result": <float>}`.

Leave the server running in the background or ready to be executed via `python3 /home/user/server.py`. Our automated test suite will send real HTTP requests to your service to verify its correctness. Use standard library modules (like `http.server` and `json`) to implement the server.