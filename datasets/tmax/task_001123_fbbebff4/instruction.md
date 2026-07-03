You are a QA engineer tasked with setting up a local test environment for our new IoT telemetry pipeline. The pipeline uses a custom C library for error-correcting checksums and state machine parsing. We are migrating our validation tooling to Rust, but for now, the Rust tool must wrap the legacy C shared library.

Currently, the test environment is broken in a few places:
1. **C Library Build Failure:** The C library in `/home/user/project/legacy_c/` fails to compile as a shared library. Fix the `Makefile` so that `make` successfully produces `libchecksum.so`.
2. **Rust Linkage Error:** The Rust CLI wrapper in `/home/user/project/rust_wrapper/` fails to compile because it cannot find the shared library at link time. Update `/home/user/project/rust_wrapper/build.rs` so that `cargo build --release` compiles successfully and links to `libchecksum.so`. The Rust CLI takes a hex string as an argument, passes it to the C library via FFI, and prints the integer checksum.
3. **Service Integration:** The test fixture uses two cooperating Python services (a device simulator and a QA aggregator). The aggregator processes data by shelling out to the Rust validator. Update `/home/user/project/services/.env` so that:
    - `VALIDATOR_BIN` points to `/home/user/project/rust_wrapper/target/release/rust_wrapper`.
    - `LD_LIBRARY_PATH` is set to include `/home/user/project/legacy_c/` so the shared library is found at runtime.

The services can be started using `/home/user/project/services/start.sh`.

Ensure that:
- `libchecksum.so` is built.
- `rust_wrapper` compiles in release mode.
- The end-to-end test suite passes when running `/home/user/project/services/test_flow.py`.

Do not modify the source code of the C library or the Rust `main.rs` file, only the build configurations and environment variables.