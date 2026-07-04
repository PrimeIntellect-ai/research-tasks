You are a build engineer managing a local artifact caching system. The system consists of a Python-based reverse proxy that intercepts artifact download requests, verifies them using a high-performance Rust helper utility, and then fetches the actual artifact from a backend storage server. 

Currently, the system is broken and incomplete. Your task is to fix the Rust code, implement the Python reverse proxy logic, and set up a robust test suite using Pytest with appropriate fixtures and mocks.

You will find the workspace at `/home/user/artifact_cache/`.

Here are your specific objectives:

1. **Fix the Rust Artifact Verifier**
   The Rust utility is located in `/home/user/artifact_cache/verifier/`. 
   If you try to compile it with `cargo build`, it will fail due to a borrow checker/ownership error. Fix the bug in `src/main.rs` so that it compiles successfully. The verifier accepts an artifact name as a command-line argument and exits with code 0 if the artifact is "valid" (for this mock, any artifact name starting with "core-" is valid, others exit with code 1).

2. **Implement the Python Reverse Proxy**
   The file `/home/user/artifact_cache/proxy.py` contains a skeleton for an HTTP server. Implement the `do_GET` method so that:
   - It listens for requests on `http://localhost:8080/download/<artifact_name>`.
   - It calls the compiled Rust verifier binary (`/home/user/artifact_cache/verifier/target/debug/verifier <artifact_name>`) using `subprocess`.
   - If the verifier exits with code 0, proxy the request to the backend storage at `http://localhost:8081/artifacts/<artifact_name>`. Return the exact content and status code from the backend server to the client.
   - If the verifier exits with a non-zero code, return an HTTP 403 Forbidden status with the body text `Invalid artifact`.

3. **Complete the Test Suite using Pytest**
   The file `/home/user/artifact_cache/test_proxy.py` is missing its test fixtures. 
   - Write a pytest fixture named `mock_backend` that starts a simple HTTP server (in a background thread) on port `8081` serving files from `/home/user/artifact_cache/backend_storage/`. Ensure it cleans up/shuts down after tests.
   - Write a pytest fixture named `proxy_server` that starts your `proxy.py` server (in a background thread) on port `8080` and shuts it down after tests.
   - The test functions are already written and rely on these fixtures.

Once you have completed the code, run the tests:
`pytest /home/user/artifact_cache/test_proxy.py -v > /home/user/test_results.log`

The task is considered successful when all tests pass, and `/home/user/test_results.log` is generated containing the successful pytest output.