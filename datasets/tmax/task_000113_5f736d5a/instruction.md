You are a build engineer responsible for migrating a legacy artifact testing pipeline to Python. 

In `/home/user/workspace`, you will find:
1. A `src` directory containing a C++ file (`main.cpp`) and a Rust file (`main.rs`).
2. An artifact API server `server.py` that accepts artifact uploads. It requires specific headers for request validation and has strict rate limiting enabled.
3. A legacy Node.js script `legacy_tester.js` that compiles the code and tests the server.

Your task is to translate this legacy orchestration and testing script into a Python script named `/home/user/workspace/test_pipeline.py`. 

The Python script must perform the following actions, mirroring the intent of the legacy script:
1. **Polyglot Build Orchestration**: Compile `/home/user/workspace/src/main.cpp` to `/home/user/workspace/artifacts/cpp_artifact` using `g++`, and compile `/home/user/workspace/src/main.rs` to `/home/user/workspace/artifacts/rust_artifact` using `rustc`. (Create the `artifacts` directory if it doesn't exist).
2. **Server Testing**: The `server.py` must be running locally on port 8080. Start it in the background before running your tests.
3. **Request Validation Testing**: The server's `/upload` endpoint requires a valid `X-Artifact-Type` header (`cpp` or `rust`). Make a POST request with the compiled `cpp_artifact` but omit the header. Verify that the server returns a `400 Bad Request` status code.
4. **Rate Limiting Testing**: The server allows a maximum of 2 requests per second. Send 3 valid POST requests (with the correct header) in rapid succession (without sleeping). Verify that the first two return `200 OK` and the third returns `429 Too Many Requests`.

Finally, your script must output its test results to a JSON file at `/home/user/workspace/test_results.json` with exactly the following boolean schema indicating whether each step succeeded:
```json
{
  "build_cpp_success": true,
  "build_rust_success": true,
  "test_validation_missing_header_success": true,
  "test_rate_limit_success": true
}
```
All keys must map to `true` if your script correctly orchestrates the build and encounters the expected server responses. Ensure your Python script runs standalone without needing external testing frameworks like `pytest`.