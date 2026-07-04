You are tasked with fixing a mathematical polyglot project located at `/home/user/math_polyglot`. The system computes the 93rd Fibonacci number using a fast iterative approach. For performance, the core math logic is written in Rust, which is meant to be compiled as a shared library and consumed by a Python orchestration script via C ABI bindings.

Currently, the project is broken and fails its End-to-End (E2E) tests. The original developer left behind three known issues you need to resolve:
1. The Rust project (`/home/user/math_polyglot/rust_math`) fails to compile into a C-compatible shared library (`.so`). The build configuration is incorrect.
2. The ABI symbol for the math function is being mangled, making it undiscoverable by the Python orchestrator.
3. The Python E2E test (`/home/user/math_polyglot/python_e2e/test_fib.py`) encounters an ABI type mismatch that yields an incorrect, truncated mathematical result.

Your tasks are:
1. Fix the `Cargo.toml` and `lib.rs` in the Rust project so that running `cargo build --release` produces `librust_math.so` in `/home/user/math_polyglot/rust_math/target/release/` with the un-mangled exported symbol `fast_fib`.
2. Debug and fix the ABI interface definition in the Python E2E script (`/home/user/math_polyglot/python_e2e/test_fib.py`) so it correctly receives the 64-bit unsigned integer result.
3. Run the Python E2E test. When successful, the Python script will automatically generate a verification file at `/home/user/e2e_success.log`.

Do not change the mathematical logic or the expected result inside the Python test file. Fix the build configuration, symbol visibility, and ABI bindings, then run the Python script to verify.