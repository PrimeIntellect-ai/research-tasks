You are acting as a systems programmer to debug a C library linking issue and deploy a math interpreter service.

We have vendored a lightweight mathematical expression interpreter library called `tinymath` at `/app/tinymath`. It is supposed to compile to a shared library (`libtinymath.so`), which is then loaded by a Python web service (`/app/server.py`) to evaluate mathematical expressions.

However, the deployment is currently broken:
1. The `tinymath` C library has a linking issue. When the Python server attempts to load the compiled shared library via `ctypes`, it fails with undefined symbol errors.
2. The Python server (`/app/server.py`) has a buggy semantic version checker. It attempts to parse the version string from `libtinymath.so` (via a `get_version()` C function) and compare it against a minimum required version (`1.2.0`), but its version comparison logic is flawed and rejects valid versions.

Your tasks are:
1. Debug the C library linking issue. Identify the missing flags in `/app/tinymath/Makefile` and fix it so that `libtinymath.so` is correctly compiled with all necessary dependencies. 
2. Create a unified diff of your changes to the Makefile and save it to `/app/makefile.patch`.
3. Fix the semantic version comparison logic in `/app/server.py` so that it correctly validates that the library version is `>= 1.2.0` using standard semantic versioning rules (e.g., `1.2.0` >= `1.2.0`, `2.0.0` >= `1.2.0`, but `1.1.9` < `1.2.0`).
4. Recompile the C library.
5. Run the Python service in the background. It must listen on `127.0.0.1:8080`.

The service acts as an HTTP API. When working correctly, a `POST` request to `http://127.0.0.1:8080/evaluate` with a JSON payload like `{"expression": "sin(0) + 1"}` will return an HTTP 200 response with `{"result": 1.0}`.

You do not need to modify the C code itself, only the build configuration and the Python wrapper. Leave the server running in the background when you are finished.