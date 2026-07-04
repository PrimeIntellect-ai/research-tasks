You are a release manager tasked with deploying a new artifact validation microservice. This service is responsible for checking the integrity of release payloads using a specialized error-correcting parity algorithm implemented in C, before they are pushed to production.

Your task consists of three parts:

1. **Repair the Vendored Library**:
   We vendor a custom C library called `libmathcheck` located at `/app/libmathcheck-1.2.4`. 
   * Apply the official security patch located at `/app/patches/CVE-2023-mathcheck.patch`.
   * The library currently fails to compile as a shared object suitable for Go's `cgo`. Fix the `Makefile` so that running `make` successfully produces `libmathcheck.so` (ensure position-independent code is used).
   * There is a memory safety bug (Undefined Behavior) in `mathcheck.c` within the `calculate_parity` function that causes incorrect parity calculations or segfaults for inputs larger than 16 bytes. Identify and fix this bug.

2. **Implement the Validation Service**:
   Create a Go HTTP service in `/home/user/release-manager/` (initialize the module as `release-manager`).
   * The service must listen exactly on `127.0.0.1:9090`.
   * It must expose a single endpoint: `POST /api/v1/release/check`.
   * The endpoint must require an `Authorization` header with the exact value: `Bearer secr3t-d3pl0y-t0k3n`. Return HTTP 401 if missing or invalid.
   * The request body will be JSON with the following schema:
     ```json
     {
       "version": "string (semantic version)",
       "payload": "string (base64 encoded data)",
       "expected_parity": "integer"
     }
     ```
   * **Semantic Versioning Check**: The service must parse the `version`. If the version is strictly less than `2.0.0-rc.1` (according to standard SemVer rules), return HTTP 426 Upgrade Required.
   * **Parity Validation**: Decode the base64 `payload`. Use `cgo` to pass the decoded byte array to the repaired `libmathcheck.so` library's `uint32_t calculate_parity(const uint8_t* data, size_t len)` function.
   * If the calculated parity matches `expected_parity`, return HTTP 200 OK with JSON `{"status": "ok"}`.
   * If it does not match, return HTTP 400 Bad Request with JSON `{"status": "mismatch"}`.

3. **Execution**:
   Once implemented, start your Go service in the background so it binds to `127.0.0.1:9090` and is ready to accept requests. Ensure it dynamically links to your compiled `libmathcheck.so` (you may need to set `LD_LIBRARY_PATH`). Write a file `/home/user/ready.txt` containing the word "READY" when your service is running.

Ensure your code handles typical errors (invalid base64, malformed JSON) by returning an HTTP 400 status code.