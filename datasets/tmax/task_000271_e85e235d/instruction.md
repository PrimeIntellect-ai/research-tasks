You are an engineer tasked with porting and benchmarking "py-smuggler", a fast C-based HTTP header smuggling fuzzer with Python bindings, to run in a minimal CI container.

Currently, the project is failing in CI. You have four main objectives:

1. **Fix the C Build System:**
   The fuzzer's core is written in C. The `Makefile` in `/home/user/smuggler/` is supposed to compile a shared library (`libsmuggler.so`), but it fails to load in Python because the object file isn't compiled as position-independent code, and the linking step is missing the shared flag. Fix the `/home/user/smuggler/Makefile` so that running `make` successfully produces a valid `/home/user/smuggler/libsmuggler.so`.

2. **Fix the Python Test Suite (Import Ordering):**
   The Python bindings are in `/home/user/smuggler/smuggler.py`, and the test suite is in `/home/user/smuggler/tests/test_smuggler.py`. The tests pass locally on the original developer's machine but fail in our clean CI environment. 
   The issue is that `smuggler.py` loads the C library upon import and immediately checks for a specific configuration environment variable (`SMUGGLER_MODE="CI"`). The test script sets this environment variable *after* importing the module. Fix `/home/user/smuggler/tests/test_smuggler.py` so the tests pass when running `cd /home/user/smuggler && python3 -m unittest discover tests`.

3. **Compile the Go Target Server:**
   There is a highly concurrent Go dummy target server in `/home/user/target/server.go`. Compile this into an executable named `server` in the `/home/user/target/` directory.

4. **Write a Performance Benchmark Script:**
   Write a Python script at `/home/user/benchmark.py` that does the following:
   - Starts the compiled Go target server (`/home/user/target/server`) as a background process (it listens on `127.0.0.1:8080`).
   - Uses the fixed `smuggler` Python module to send fuzzed requests. The `smuggler.py` module exposes a function `send_fuzz(host, port) -> int` which sends a single payload and returns `1` on success.
   - Run a benchmark loop for exactly 3 seconds, calling `send_fuzz("127.0.0.1", 8080)` as many times as possible sequentially.
   - Gracefully terminate the Go server process.
   - Write a JSON file to `/home/user/benchmark.json` containing exactly these keys:
     - `"status"`: `"success"`
     - `"duration"`: the actual elapsed time in seconds (float)
     - `"requests_sent"`: the total number of successful requests sent (integer)

Ensure all files are created or modified exactly at the specified paths. You may run any commands in your terminal to build, debug, and test the code.