You are helping a developer migrate a polyglot mathematical microservice from a legacy setup. 
The system consists of a Rust backend that computes Fibonacci numbers and a Python reverse proxy that fronts the service. The developer is migrating the proxy from Python 2 to Python 3.

Here is your task:
1. Navigate to `/home/user/rust_backend`. There is a logical bug in the mathematical computation in `src/main.rs`. Apply the provided patch file `/home/user/rust_backend/fix_math.patch` to fix the math logic.
2. Build the Rust backend using `cargo build --release`.
3. The reverse proxy is located at `/home/user/proxy.py`. It is currently written in Python 2. Upgrade the script so that it works correctly with Python 3. You will need to update the syntax and standard library imports (e.g., `BaseHTTPServer` and `urllib2` replacements).
4. Start the compiled Rust backend server in the background (it will listen on `127.0.0.1:8080`).
5. Start your updated Python 3 reverse proxy in the background (it will listen on `127.0.0.1:8000` and proxy requests to `8080`).
6. Finally, run the provided integration test script `/home/user/test_integration.py` (which is already in Python 3). It will send a request to the proxy and write the result to `/home/user/test_results.txt`.

Ensure all servers are running before executing the integration test. The automated test will verify the contents of `/home/user/test_results.txt` to confirm that the patch was applied and the proxy forwards requests successfully.