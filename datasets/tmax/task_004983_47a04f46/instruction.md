You are an integration developer responsible for testing a newly written local API that acts as a frontend for a legacy C-based bytecode emulator.

In your home directory (`/home/user`), you have the following files:
1. `vm.c`: A C library implementing a tiny stack-based emulator. It contains a function `int evaluate(const char* bytecode)`.
2. `Makefile`: A makefile to build the C code into a shared object (`libvm.so`).
3. `api.py`: A Python 3 HTTP server that uses `ctypes` to load `libvm.so` and exposes an endpoint `/eval` which accepts a GET request with a `code` query parameter.

Currently, the system is broken. The original developer wrote `api.py` but forgot to properly configure the Foreign Function Interface (FFI) bindings for the C function (specifically, setting the correct argument types and return type for `lib.evaluate`, and passing properly encoded bytes).

Your task is to:
1. Build the shared library using the provided `Makefile`.
2. Fix the FFI binding and URL parameter handling bugs in `api.py` so that it correctly passes the bytecode string to the C library and retrieves the integer result.
3. Start the API server on port 8080 in the background.
4. Write and execute a test script to send a GET request to `http://localhost:8080/eval` with the query parameter `code` set to `P8M3P4`.
5. Save the raw text response of the successful HTTP request strictly into `/home/user/result.log`.

Do not change the API endpoint path or port. The final result should be accurately calculated by the C emulator and captured in the log file.