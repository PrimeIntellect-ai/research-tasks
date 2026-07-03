You are a mobile build engineer maintaining a cross-platform build pipeline. A major bottleneck in our pipeline orchestration is resolving the latest compatible mobile SDK versions from a massive list of available releases. The current Python-based semantic version parser is too slow for our real-time dependency resolver.

Your task is to optimize this by rewriting the core semantic version logic in C and wrapping it in a polyglot REST API.

Here are your instructions:

1. **Workspace setup**: Work inside `/home/user/mobile_pipeline/` (create it if it doesn't exist).

2. **C Semantic Version Library**: 
   Write a C file named `semver.c`. Implement a custom data structure and parsing logic to compare semantic versions (MAJOR.MINOR.PATCH). 
   You must implement the following C function signature:
   `const char* get_latest_version(const char** versions, int count);`
   - It takes an array of semantic version strings and the count of strings.
   - It returns the highest semantic version from the array.
   - Semantic versions follow the standard `X.Y.Z` format (e.g., `2.10.5` is greater than `2.2.0`). You do not need to handle pre-release or build metadata (no hyphens or plus signs).

3. **Polyglot Build Orchestration**:
   Create a `Makefile` that compiles `semver.c` into a shared library named `libsemver.so`. The build should use standard GCC optimizations (`-O3`). 

4. **REST API Construction**:
   Write a Python 3 script named `resolver_api.py`.
   - It must load `libsemver.so` using the `ctypes` module.
   - It must run a basic HTTP server (using the standard library `http.server`, no external frameworks like Flask allowed) listening on `127.0.0.1` port `8080`.
   - It must expose a `POST /resolve` endpoint.
   - The endpoint will receive a JSON payload with a list of versions: `{"versions": ["1.2.3", "2.10.0", "2.2.5"]}`.
   - It must pass this list to the C `get_latest_version` function.
   - It must return a JSON response with the highest version: `{"latest": "2.10.0"}`.

5. **Logging**:
   When your `resolver_api.py` server starts and is ready to accept connections, it must write the exact string `[API READY] Server listening on port 8080` to a log file at `/home/user/mobile_pipeline/pipeline.log`.

Ensure your server runs continuously in the background so it can be tested. You can test it yourself using `curl`.