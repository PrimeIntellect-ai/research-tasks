I am migrating a legacy Python 2 application to Python 3. The application relies on a custom C library for high-performance string manipulation, but the build setup is broken and the Python wrapper is completely incompatible with Python 3 due to syntax and bytes/string ABI (ctypes) changes.

I need you to fix the build system, upgrade the Python wrapper, and create a REST API to expose this library. 

Here are your instructions:

1. **Fix the Makefile**: 
   Navigate to `/home/user/legacy_app`. There is a `Makefile` that is supposed to build a shared library `libprocessor.so` from `processor.c`. It is currently broken and fails to produce a valid dynamically linked shared object. Fix the `Makefile` so that running `make` successfully compiles `libprocessor.so`.

2. **Migrate the Python wrapper**:
   In the same directory, there is `wrapper.py` written in Python 2. Update it to be fully compatible with Python 3. 
   - Fix any Python 2 syntax errors.
   - The `transform(text)` function must take a standard Python 3 `str` and return a standard Python 3 `str`.
   - Properly handle the ABI boundaries: `ctypes` in Python 3 requires explicit byte conversions when interacting with C `char*` arrays. Ensure no `TypeError` or memory corruption occurs.

3. **Construct a REST API**:
   Create a new file `/home/user/legacy_app/api.py`. 
   Using ONLY Python 3's built-in standard libraries (e.g., `http.server`, `json`, `urllib`), create a web server listening on `127.0.0.1` port `8000`.
   - The server must expose a single `GET` endpoint: `/api/transform`
   - It should accept a query parameter `text` (e.g., `/api/transform?text=helloworld`).
   - It must import and use the `transform` function from `wrapper.py` to process the text.
   - It must return a JSON response in this exact format: `{"result": "<transformed_string>"}`. Ensure the `Content-Type` header is set to `application/json`.

4. **Run the API**:
   Start your server in the background and write its process ID (PID) to `/home/user/api.pid`. Make sure the server is actually running and binding to the port before finishing.