I am building a high-performance Python web service that acts as a mini Web Application Firewall (WAF) emulator. It uses a custom C library (`libwaf.so`) to perform state-machine-based payload analysis and checksum validation. However, I am stuck on a C library linking issue, and the API routing is incomplete. 

Here is the current state of my project in `/home/user/waf_project/`:

1. `waf.c`: The C source code containing the security state machine and checksum validator.
2. `build.sh`: A shell script meant to compile `waf.c` into a shared object (`libwaf.so`). Right now, it produces an invalid ELF file or fails to link properly because of missing compiler flags.
3. `api.py`: A FastAPI application that is supposed to load the C library, receive HTTP POST requests, compute a specific checksum, and pass the data to the C function.
4. `requirements.txt`: Contains `fastapi` and `uvicorn`.

Your tasks:
1. Fix `build.sh` so that it correctly compiles `waf.c` into a shared library `libwaf.so` that can be loaded via Python's `ctypes`. Run the build script.
2. Fix `api.py`:
   - Correctly load `./libwaf.so` using `ctypes`.
   - Set up the correct `argtypes` and `restype` for the `analyze_payload` C function. The function signature is `int analyze_payload(const char* payload, uint32_t checksum);`.
   - Implement a POST route `/analyze` that accepts a JSON body: `{"data": "<string>"}`.
   - In the route, calculate the checksum for the payload. The C library expects the checksum to equal `length(data) * 42`.
   - Call the C function. The C function returns `-1` for invalid checksum, `0` for safe payload, and `1` for malicious payload.
   - Return a JSON response: `{"status": "<result>"}` where `<result>` is `"checksum_error"`, `"safe"`, or `"malicious"`.
3. Start the FastAPI server on `127.0.0.1:8000` in the background.
4. Create a test script `/home/user/test_waf.py` that sends a POST request to `http://127.0.0.1:8000/analyze` with the payload `{"data": "GET / HTTP/1.1\nHost: example.com\nSELECT * FROM users;"}`.
5. Have the test script save the exact JSON response from the API to `/home/user/result.json`.

Please ensure all dependencies are installed and the final result file is generated correctly.