You are a web developer building a secure authentication API. The project uses a Python (Flask) backend but offloads sensitive cryptographic hashing to a legacy C library for performance and security reasons.

The project is located at `/home/user/auth_project`.

Currently, the project is broken in three ways:
1. **Dependency Conflict:** The `requirements.txt` file contains conflicting versions of web framework dependencies that prevent the server from starting or installing correctly.
2. **Missing Build Orchestration:** The C library needs to be compiled into a shared object, but there is no build script.
3. **Missing API & E2E Tests:** The backend application and tests are incomplete.

Your tasks are to fix these issues and orchestrate the full build and test pipeline:

1. **Resolve Dependencies:** Modify `/home/user/auth_project/requirements.txt` so that it installs a compatible combination of `Flask` and `Werkzeug` (e.g., Flask 2.2.0 requires Werkzeug < 3.0).
2. **Polyglot Build Script:** Write a Python script at `/home/user/auth_project/build_polyglot.py` that, when executed, compiles the C source code located at `/home/user/auth_project/src/c_crypto/crypto.c` into a shared library at `/home/user/auth_project/lib/libccrypto.so`. Use `gcc` via Python's `subprocess` module. Ensure the `/home/user/auth_project/lib/` directory is created if it doesn't exist.
3. **Web Server:** Write a Flask application at `/home/user/auth_project/app.py` that:
    - Exposes a `POST /hash` endpoint.
    - Accepts a JSON payload: `{"password": "<string>"}`.
    - Uses Python's `ctypes` module to load `/home/user/auth_project/lib/libccrypto.so`.
    - Calls the C function `void compute_hash(const char* input, char* output)` with the provided password. Assume the output buffer needs a maximum of 256 bytes.
    - Returns a JSON response: `{"hash": "<computed_string>"}`.
4. **End-to-End Test Orchestration:** Write a Python script at `/home/user/auth_project/test_e2e.py` that:
    - Starts the `app.py` Flask server in a background process (running on port 5000).
    - Waits for the server to become healthy/available.
    - Sends a POST request to `http://127.0.0.1:5000/hash` with the payload `{"password": "test_password_123"}`.
    - Saves the exact JSON response to `/home/user/auth_project/test_results.json`.
    - Gracefully terminates the background Flask process before exiting.

Execute your `build_polyglot.py` to build the library, and then execute `test_e2e.py` to generate the test results.