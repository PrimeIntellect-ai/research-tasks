You are an engineer setting up a minimal polyglot build system from scratch. In `/home/user/polyglot/`, there are two files:
1. `algo.c`: A C file implementing a simple numerical algorithm (moving average).
2. `wrapper.py`: A Python wrapper that loads the C library via FFI (`ctypes`) and implements a mock request validation/rate-limiting decorator.

Currently, the setup is broken in a few ways:
1. The C code has not been compiled into a shared library.
2. The Python wrapper is missing the correct FFI definitions (`argtypes` and `restype`) for the `moving_average` function.
3. The rate limiting logic in `wrapper.py` is flawed; it blocks the very first request instead of allowing the first and rate-limiting subsequent ones within the time window.

Your task is to fix this environment using standard shell commands and tools:
1. Compile `algo.c` into a shared library named `libalgo.so` in the same directory.
2. Fix the FFI signatures in `wrapper.py`. The C function signature is `double* moving_average(double* data, int len, int window)`.
3. Fix the rate-limiting logic in `wrapper.py` so that it allows the execution to proceed.
4. Execute the patched `wrapper.py`.
5. Save the standard output of the successful run of `wrapper.py` to `/home/user/polyglot/success.txt`.

You can use standard Linux utilities (like `gcc`, `sed`, `awk`, `python3`, or simple text editors if you prefer).