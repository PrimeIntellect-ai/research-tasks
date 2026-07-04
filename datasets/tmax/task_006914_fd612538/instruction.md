You are a systems programmer debugging a C library linking issue in a Rust project. 

You have a Rust crate located at `/home/user/rust-linker-debug` that acts as a safe FFI wrapper around a static C library, `libops.a`, located in `/home/user/clib`. 

Recently, the C library was upgraded to version `2.1.3`. In version 2.x, the C API changed the signature of its primary multiplication function from `int ops_mul(int a, int b)` to `int ops_mul_v2(int a, int b, int flags)`.

Currently, the Rust crate fails to compile/link because it's still trying to link against the v1 API. 

Your tasks are:
1. **Fix the build script (`build.rs`)**: 
   - Parse the structured JSON file at `/home/user/clib/manifest.json`.
   - Extract the `"version"` field.
   - Use semantic version comparison (the `semver` and `serde_json` crates are available in `Cargo.toml`) to check if the major version is `>= 2`.
   - If it is, output the conditional build flag: `cargo:rustc-cfg=use_v2`.
   - Ensure the build script still correctly tells cargo where to find the static library (link search path `/home/user/clib` and static lib `ops`).

2. **Fix the conditional compilation (`src/lib.rs`)**:
   - The FFI wrapper `safe_mul` is missing the correct conditional compilation flags (`#[cfg(use_v2)]` and `#[cfg(not(use_v2))]`). Update `src/lib.rs` to properly declare and call `ops_mul_v2(a, b, 0)` when `use_v2` is active, and `ops_mul(a, b)` otherwise.

3. **Implement Property-Based Testing**:
   - Inside `src/lib.rs`, there is an empty `tests` module. Use the `proptest` crate (already listed in `Cargo.toml`) to write a property-based test named `test_mul_properties`.
   - The test should generate two random `i32` values (each between -1000 and 1000) and assert that `safe_mul(a, b) == a * b`.

Once you have implemented these fixes, run the tests and save the output to verify your work.
Execute: `cargo test -- --nocapture > /home/user/test_results.log 2>&1`

The automated test will inspect `/home/user/test_results.log` for the successful execution of your property test, and it will verify that your `build.rs` properly parses the JSON and sets the semantic version flags.