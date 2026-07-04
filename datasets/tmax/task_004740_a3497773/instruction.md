You are a mobile build engineer maintaining the pipeline infrastructure for a large mobile application. Part of our dynamic configuration system relies on a vendored C library called `libexpr`, which evaluates arithmetic feature-flag expressions. 

Recently, a bad merge broke the vendored package. We need you to repair the build system, fix a critical memory safety bug, prove it is fixed with property-based testing, and expose the library via a Python HTTP service for our build workers.

Here are your specific tasks:

1. **Fix the Build System (Polyglot Build Orchestration)**
   The `libexpr` source code is vendored at `/app/vendor/libexpr/`. Currently, running `make` fails because of a circular dependency perturbation in the `Makefile`. Identify and resolve this dependency loop so that `make` successfully produces the shared library `/app/vendor/libexpr/libexpr.so`.

2. **Fix the Memory Safety Issue**
   The C code in `/app/vendor/libexpr/parser.c` contains a buffer overflow vulnerability (Undefined Behavior) when parsing large expressions. Fix the C code so it safely handles expressions of any length up to 1024 characters without memory corruption (e.g., using safe string bounds).

3. **Write a Property-Based Test**
   In `/home/user/test_expr.py`, write a Python property-based test using the `hypothesis` library. The test should load `libexpr.so` via `ctypes` and use `@given(strategies.text())` to verify that passing arbitrary strings to the C evaluation function does not cause a segmentation fault. (You do not need to run this continuously, but you must create the file to demonstrate the fix).

4. **Implement the HTTP Microservice (URL routing & parameter parsing)**
   Write and start a Python HTTP server (e.g., using the built-in `http.server` or `Flask`) that listens on `0.0.0.0:8080`.
   - It must expose a single endpoint: `GET /eval`
   - It should accept a query parameter `expr` (e.g., `/eval?expr=5%2B5`).
   - It must pass the decoded expression string to the `libexpr.so` evaluate function.
   - It must return an `application/json` response: `{"result": <integer>}` if successful, or `{"error": "Invalid"}` if the C function returns an error code or fails.
   
Keep the HTTP server running in the foreground or background so that our automated verifier can test it. 

Constraints:
- Do not change the core evaluation logic in C (addition and subtraction), only fix the memory bug and Makefile.
- The C function signature is `int evaluate_expression(const char* expr, int* out_result);`. It returns `0` on success and `-1` on error.
- Your HTTP service must run on port 8080.