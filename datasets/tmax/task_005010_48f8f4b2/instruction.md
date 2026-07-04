I am developing a high-performance script utility for analyzing semantic versions, but I'm running into some issues with a third-party C extension and need you to fix it, test it, and wrap it in a web service.

You will find the source code for a C-based Python extension vendored at `/app/semver_fast-1.0.0`. This package provides a fast semantic version parsing and comparison module, but it has a couple of critical flaws:
1. It crashes with memory corruption (undefined behavior) when comparing complex pre-release version strings (e.g., `1.0.0-alpha.beta.reallylongstring.1234567890`). Analyze the C code to identify and repair the memory safety issue (look for fixed-size buffer overflows or improper string handling).
2. The `setup.py` file has a configuration error preventing it from compiling cleanly. Fix it so you can install the module into the system Python environment (e.g., `pip install -e /app/semver_fast-1.0.0`).

Once you have fixed and installed the `semver_fast` extension:
1. Write a property-based test script at `/home/user/test_semver.py` using the `hypothesis` library. It must generate arbitrary valid semantic version strings and assert that `semver_fast.compare(v1, v2)` behaves identically to Python's built-in `packaging.version.parse()`. You don't need to run this for me, but save it correctly.
2. Create and start a Python HTTP server script at `/home/user/semver_server.py`. The server must listen on `127.0.0.1:8888` and implement the following two REST endpoints:
   - `POST /sort`: Accepts a JSON payload like `{"versions": ["2.0.0", "1.0.5", "1.0.0-alpha"]}`. It must use `semver_fast` to sort the versions in ascending order and return a JSON payload `{"sorted": ["1.0.0-alpha", "1.0.5", "2.0.0"]}`.
   - `POST /diff`: Accepts a JSON payload `{"base": ["1.0.0", "1.1.0"], "target": ["1.1.0", "1.2.0"]}`. It must return a sorted list of versions that are present in `target` but *missing* from `base`. Output format: `{"diff": ["1.2.0"]}`.

Start the server in the background so it is running when your turn ends. Ensure the server strictly uses `semver_fast` for its internal sorting logic, as standard libraries will be too slow for our production workload. Keep the server running!