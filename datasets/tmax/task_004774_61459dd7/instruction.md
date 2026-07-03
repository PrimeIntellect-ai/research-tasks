You are an integration developer tasked with fixing and completing a secure API gateway written in Rust. The project is located at `/home/user/api-gateway`. 

Currently, the project fails to compile due to a dependency version conflict in `Cargo.toml` (similar to a peer dependency error in Node.js, but with Rust crates). The gateway is designed to bridge a legacy REST webhook system with a new gRPC microservice architecture.

Your tasks are to:
1. **Fix Dependencies:** Resolve the version conflict between `tonic`, `prost`, and `tonic-build` in `Cargo.toml` so the project successfully compiles. Do not change the general architecture or remove core crates.
2. **Implement REST Routing & Checksum:** Complete the Axum REST handler in `src/rest.rs`. It must handle `POST` requests to `/api/v1/relay/:id`. 
   - Extract the `:id` parameter from the URL.
   - Extract the `X-Checksum` header (which contains a CRC32 checksum of the raw request body as an unsigned 32-bit integer string).
   - Compute the CRC32 checksum of the incoming raw body.
   - If the checksum matches, return a `200 OK` and (conceptually) prepare the gRPC forward request (the gRPC client code is stubbed out for you, just call the provided stub function).
   - If the checksum fails or the header is missing/invalid, return a `400 Bad Request`.
3. **Write Property-Based Tests:** In `src/security_tests.rs`, write a property-based test using the `proptest` crate. The test must generate random string payloads, compute their valid CRC32 checksums, and verify that your routing logic accepts valid payload/checksum pairs and rejects invalid ones.
4. **Verification:** Once everything is fixed and implemented, run the test suite and output the results to a log file:
   `cargo test > /home/user/test_results.log 2>&1`

The automated test suite will read `/home/user/test_results.log` to verify that all tests pass, including your new proptest.