You are a platform engineer maintaining our CI/CD pipelines. Our latest pipeline run is failing during the build and test phases of a hybrid C/Rust project. 

The project consists of a C application (`runner`) that evaluates custom rate-limiting rules using a Rust-based shared library (`librate_eval.so`). 

There are three main issues you need to resolve in `/home/user/project`:

1. **Shared Library Linkage (CMake):** 
   The `CMakeLists.txt` in `/home/user/project` is failing at link time. It cannot find the Rust shared library. The Rust library is built into `/home/user/project/rust_lib/target/release/`. Fix the `CMakeLists.txt` so it correctly locates and links `librate_eval`.

2. **Interpreter & ABI Implementation (Rust):**
   The C program expects an ABI-compatible function from the Rust library:
   `int evaluate_rule(const char* rule_str, int request_count);`
   
   You must implement this function in `/home/user/project/rust_lib/src/lib.rs`. 
   The function acts as a simple interpreter for rate-limiting rules. The `rule_str` will be a string in the format `"MAX:<number>"`, where `<number>` is a non-negative integer. 
   - If `request_count <= number`, return `1` (Allowed).
   - If `request_count > number`, return `0` (Denied).
   - If `rule_str` is invalid, null, or cannot be parsed, return `-1` (Error).

3. **Property-Based Testing (Rust):**
   Add a property-based test using the `proptest` crate in your Rust library. 
   Write a test named `test_evaluate_rule_properties` that generates random valid rule strings (`"MAX:<N>"`) for `N` between 0 and 1000, and `request_count` between 0 and 1500, verifying that the function correctly returns `1` or `0` according to the logic above. Add `proptest` to `/home/user/project/rust_lib/Cargo.toml` as a dev-dependency.

Once you have fixed the code:
1. Run `cargo build --release` in the `rust_lib` directory.
2. Run `cargo test` in the `rust_lib` directory and redirect the output to `/home/user/cargo_test.log`.
3. Create a `build` directory in `/home/user/project`, run `cmake ..`, and `make`.
4. Run the resulting `runner` executable and save its standard output to `/home/user/runner_output.log`.

The setup script has already created the skeleton files. Modify them to meet the requirements.