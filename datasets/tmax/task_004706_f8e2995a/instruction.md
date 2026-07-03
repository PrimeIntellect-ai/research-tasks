You are a build engineer managing artifacts for our internal authentication services. We have a multi-service authentication backend consisting of a Python-based frontend API and a metrics aggregation service. The Python API delegates heavy cryptographic token parsing to a C library (`libtoken.so`) using FFI (`ctypes`).

Currently, the system is broken in multiple ways:
1. **Build Failure:** The `Makefile` in `/home/user/app/` has a circular dependency that prevents building the shared object `libtoken.so` from `src/token.c` and `src/crypto.c`.
2. **Memory Safety & Serialization:** The token verification function in `src/token.c` receives a serialized binary string from Python but suffers from a memory safety vulnerability (a buffer overflow) when copying the username from the payload. This causes the Python service to crash with a Segmentation Fault when subjected to long inputs.

Your task:
1. Fix the `Makefile` in `/home/user/app/` to resolve the circular dependencies so that running `make` successfully produces `libtoken.so`.
2. Fix the buffer overflow in `src/token.c`. The `verify_token` function must safely handle inputs larger than its internal 16-byte username buffer without crashing. (It should truncate or safely reject oversized inputs, returning 0 on failure or 1 on success).
3. Recompile the C library by running `make`.
4. Ensure the Python API (`/home/user/app/api.py`) is running on `127.0.0.1:8080` and the metrics service (`/home/user/app/metrics.py`) is running on `127.0.0.1:8081`. Both are started via a wrapper script `/home/user/app/start_services.sh`. You will need to restart them after building the new library.

Ensure that the web services remain running in the background so our integration tests can communicate with them over HTTP.