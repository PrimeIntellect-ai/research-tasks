You are acting as a release manager preparing a new deployment for our data pipeline. We have a vendored C-extension-backed Python package located at `/app/vendored_data_parser` that is currently broken due to a recent system upgrade. Once the package is fixed, you need to implement a small HTTP API service that uses this package to parse incoming data and perform semantic version checks.

Your tasks are to:

1. **Fix the Vendored Package (ABI / Shared Library Issue)**:
   The package at `/app/vendored_data_parser` contains a compiled shared object (`data_parser.so`). The `Makefile` was perturbed and currently builds the shared library with the wrong ABI flags (it links against an outdated fake library version). Fix the `Makefile` so it builds correctly, and ensure the Python package is usable in the current environment. 

2. **Implement Semantic Version Comparison**:
   Write a Python module `/home/user/schema_validator.py` that imports `vendored_data_parser`. You must write a function `is_compatible(requested_version: str, available_version: str) -> bool` that strictly adheres to Semantic Versioning 2.0.0. The function must return True if the `requested_version` is backward compatible with the `available_version` (i.e., same major version, and minor version of available is >= requested; patch version must be >= if minor is equal). 

3. **Property-Based Testing**:
   Write a property-based test script using the `hypothesis` library at `/home/user/test_schema_validator.py` to test your `is_compatible` function. Ensure your tests verify that an available version with a lower major version than the requested version always returns `False`. Save the test execution log to `/home/user/test_results.log`.

4. **Deploy the API Service**:
   Create and start a Python HTTP service (e.g., using `http.server` or `Flask` if available in the standard environment, or bare sockets) listening on `127.0.0.1:8080`.
   - The service should expose a `POST /validate` endpoint.
   - It should expect JSON payloads: `{"data": "<hex_encoded_data>", "schema_version": "<semver>"}`.
   - It must first use `schema_validator.is_compatible` against an internal available schema version `2.4.1`.
   - If incompatible, return HTTP 400.
   - If compatible, use `vendored_data_parser.parse_hex(data)` to parse the hex string. Return an HTTP 200 with JSON: `{"status": "success", "parsed": <result_from_parser>}`.
   - The service MUST require a Bearer token in the Authorization header: `Authorization: Bearer release-manager-token-992`. Requests without this exact token must return HTTP 401.

Ensure the service remains running in the background so our integration tests can verify it. Write the PID of the service to `/home/user/service.pid`.