You are acting as a systems programmer working on a web security module. We have a Rust library, `sec-payload-verifier`, located at `/home/user/sec-payload-verifier`. This library is responsible for validating the integrity of incoming web payloads using a custom checksum algorithm written in C (`src/fast_chk.c`), which we are binding to via FFI. 

Currently, the property-based tests (using the `proptest` crate) in `src/lib.rs` are failing to compile and link because the build script (`build.rs`) is broken and doesn't compile the C code. Furthermore, we lack a CI/CD pipeline to ensure these property tests run automatically on GitHub.

Your tasks are:
1. Fix `/home/user/sec-payload-verifier/build.rs` using the `cc` crate so that it compiles `src/fast_chk.c` and statically links it to the Rust project as `fast_chk`.
2. Create a GitHub Actions workflow file at `/home/user/sec-payload-verifier/.github/workflows/ci.yml`. It should trigger on `push`, run on `ubuntu-latest`, and include a step that executes `cargo test`.
3. Verify your fix locally by navigating to `/home/user/sec-payload-verifier` and running `cargo test`. Save the standard output and standard error of this test run to `/home/user/test_results.log`.

Ensure that the tests pass successfully and the log file reflects a successful test run.