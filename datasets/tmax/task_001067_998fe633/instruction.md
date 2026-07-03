You are an open-source maintainer reviewing a pull request that was supposed to optimize our project's C++ mathematical hashing library and its Python API integration. Unfortunately, the contributor broke almost everything.

The project consists of a C++ shared library that implements a fast hashing algorithm (djb2 variant), a C++ CLI wrapper, and a Python Flask API that uses the C++ library via `ctypes` and caches results in Redis.

Here is what you need to fix in `/home/user/workspace`:

1. **Build System & Compilation**: The `CMakeLists.txt` is broken. It fails to compile the shared library `libmathops.so` and the CLI wrapper `compute_hash`. Fix the CMake configuration so that running `cmake . && make` in `/home/user/workspace/build` successfully generates both targets.
2. **C++ Math Bug**: The contributor tried to optimize the loop in `src/hash.cpp` but altered the mathematical behavior of the hash function. We have a stripped reference binary at `/home/user/oracle_hash` that implements the correct behavior. You must fix the C++ code so that the output of your `compute_hash` CLI is bit-exact equivalent to `oracle_hash` for any input string.
3. **FFI Interop**: The Flask application in `api/app.py` loads `libmathops.so` using `ctypes`. The PR broke the `argtypes` and `restype` definitions, causing segfaults or garbage output. Fix the FFI bindings.
4. **Service Integration**: The Flask API should connect to a local Redis instance on port 6379 to cache results. The environment variables or connection strings in `api/app.py` might be missing or incorrect. Fix them.

Once the code is fixed, you must ensure the full stack is running:
- Start the Redis server on the default port.
- Compile the C++ code into the `build` directory.
- Start the Flask app (`python3 api/app.py`) so it listens on `127.0.0.1:5000`.

The API has a single endpoint: `POST /hash` taking form data `data=<string>`. It must return a JSON response: `{"hash": <integer>, "cached": <boolean>}`. 

You do not need to write a benchmarking script yourself, but the correct implementation of the hash function is crucial. Ensure your services are running in the background before you complete the task.