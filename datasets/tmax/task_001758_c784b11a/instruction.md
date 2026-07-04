You are a QA engineer setting up a test environment for a Go application that uses a Rust shared library via CGo. The project is located in `/home/user/test_env`.

Currently, the test suite is failing due to three cascading issues:
1. **Rust Compile Error:** The Rust library in `/home/user/test_env/rust_src` has an ownership/borrow-checker bug in `src/lib.rs` that prevents compilation. It is supposed to expose a C-compatible function `get_version()` returning a static string `"1.5.2"`.
2. **Linker Error:** Even if the Rust library compiles, the Go application in `/home/user/test_env/go_app` cannot find the shared library (`libversion_check.so`) at link/run time because the library search path is not properly configured in the environment when running the tests.
3. **Test Fixture Setup:** The Go test uses a state-machine semantic version parser and requires a specific test fixture configuration, specifically the environment variable `STRICT_SEMVER=1`, to run properly.

Your task:
1. Fix the borrow checker bug in `/home/user/test_env/rust_src/src/lib.rs` so it safely returns a valid C string pointer.
2. Build the Rust project as a shared library (`cargo build`).
3. Run the Go test suite in `/home/user/test_env/go_app` ensuring that the linker can find the compiled shared library (e.g., via `LD_LIBRARY_PATH`) and the `STRICT_SEMVER=1` environment variable is set.
4. Save the verbose output of the successful Go test run (`go test -v`) to `/home/user/test_output.log`.