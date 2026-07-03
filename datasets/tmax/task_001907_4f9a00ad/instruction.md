You are a developer picking up a partially completed Rust project that acts as a REST API wrapper around a highly optimized C library. 

Currently, the workspace is disorganized. The C library compiles via CMake, but the Rust API fails to link to it. Furthermore, there are no tests ensuring the algorithmic correctness of the API. 

Your goal is to organize the build, link the shared library properly, write a property-based test, and orchestrate an end-to-end (E2E) testing script.

Here is the current state of `/home/user/workspace`:

1. `/home/user/workspace/c_math/`
   - `CMakeLists.txt`: A standard CMake file that defines a shared library target `cmath`.
   - `cmath.c`: Contains two functions: `int add(int a, int b);` and `int sub(int a, int b);`.

2. `/home/user/workspace/api/`
   - `Cargo.toml`: A Rust project configured with `axum`, `tokio`, `serde`, `reqwest`, and `proptest`.
   - `src/main.rs`: An Axum REST server with `POST /add` and `POST /sub` endpoints. It declares `extern "C"` bindings for `add` and `sub`. 

**Your tasks:**

1. **Build the Shared Library:**
   Manually compile the CMake project in `/home/user/workspace/c_math/` so that it produces the `libcmath.so` shared library in `/home/user/workspace/c_math/build/`.

2. **Fix the Linker Issue:**
   The `api` project fails to build because it cannot find the `cmath` library. Create a `build.rs` file in `/home/user/workspace/api/` to emit the correct `cargo:rustc-link-search` and `cargo:rustc-link-lib` instructions so Cargo knows where to find `libcmath.so` during the build.

3. **Implement Property-Based E2E Tests:**
   Create `/home/user/workspace/api/tests/e2e_test.rs`. 
   Using the `proptest` crate and `reqwest::blocking::Client`, write a property-based test named `test_add_sub_inverse`.
   The test should generate random `i32` pairs `(a, b)` in the range `-1000..1000`. 
   For each pair, send a JSON `POST` to `http://127.0.0.1:3000/add` with `{"a": a, "b": b}`. Extract the `result` (let's call it `sum`). Then send a `POST` to `http://127.0.0.1:3000/sub` with `{"a": sum, "b": b}`. 
   Assert that the final result equals the original `a`.

4. **Orchestrate the Test Run:**
   Create an executable bash script at `/home/user/workspace/run_all.sh`.
   When executed, this script must:
   - Export `LD_LIBRARY_PATH` appropriately so the shared library can be found at runtime.
   - Start the Rust API server (`cargo run --manifest-path api/Cargo.toml`) in the background.
   - Wait 2 seconds for the server to initialize.
   - Run the property-based tests (`cargo test --manifest-path api/Cargo.toml --test e2e_test`).
   - Terminate the background API server.
   - If the tests pass, write the exact string `SUCCESS` to `/home/user/workspace/status.txt`. If they fail, write `FAILED`. Exit with code 0 in either case.

Do not modify `src/main.rs` or the C source files.