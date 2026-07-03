You are a release manager preparing a hybrid C/Python mathematical microservice for deployment. The service evaluates the function f(x, y) = x³ + y² - x*y for high-performance workloads, relying on a C backend for speed and a Python frontend for the HTTP API. 

The previous developer left the codebase incomplete. Your task is to finish the build orchestration, cross-language bindings, and URL routing, then start the service and verify it.

The workspace is located at `/home/user/app`. Inside, you will find:
1. `/home/user/app/math_core.c`: The C implementation of the math function.
2. `/home/user/app/server.py`: The incomplete Python web server.

Perform the following steps:
1. **Polyglot Build:** Compile `/home/user/app/math_core.c` into a shared library named `/home/user/app/libmathcore.so`.
2. **FFI Integration:** Edit `/home/user/app/server.py` to load `libmathcore.so` using Python's `ctypes`. Ensure you set the `argtypes` and `restype` of the `evaluate` function correctly (both inputs and the output are C `double`).
3. **URL Routing:** Complete the `do_GET` method in `/home/user/app/server.py`. It must intercept requests to the path `/eval`. It should parse the query string parameters `x` and `y` as floats, pass them to the C function, and respond with an HTTP 200 status and the exact text `Result: <value>` (where `<value>` is the float returned by the C function). For any other path, it can return a 404.
4. **Service Startup:** Run the Python server in the background so it listens on port 8080.
5. **Verification:** Use `curl` to test the endpoint with `x=4.0` and `y=3.0`. Save the raw output of this curl command to `/home/user/app/release_test.log`.

Do not change the directory structure. Your final state should have the server running in the background, the `.so` file compiled, and the log file generated.