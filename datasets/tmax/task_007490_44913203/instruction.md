You are tasked with fixing and integrating a polyglot encoding system located in `/home/user/polyglot_system`. The system consists of a Rust library, a concurrent Go command-line service, and a Python test orchestrator. Currently, the Rust project fails to compile, the Go service has a concurrency bug, and the Python test suite needs to be written.

Here is the current state of the system and what you must do:

1. **Fix the Rust Component (`/home/user/polyglot_system/rust_encoder`)**
   The Rust library is intended to expose a C FFI function `encode_hex(input: *const c_char, output: *mut c_char)` that takes a UTF-8 string and converts it to a hexadecimal string. Currently, it fails to compile or link correctly as a C FFI because it is missing the correct FFI attributes and keywords. Fix `src/lib.rs` so it can be built as a `cdylib`.

2. **Fix the Go Component (`/home/user/polyglot_system/go_encoder/main.go`)**
   The Go program takes a string as a CLI argument, splits it into characters, processes them concurrently using goroutines and channels to hex-encode them, and prints the joined result. However, it currently hangs due to a channel deadlock (a channel is never closed before a `range` loop). Fix the deadlock so it prints the encoded string and exits successfully.

3. **Build Orchestration (`/home/user/polyglot_system/build.sh`)**
   Write a bash script at `/home/user/polyglot_system/build.sh` that compiles both projects:
   - Compile the Rust project to a shared object library (`librust_encoder.so`) located in `/home/user/polyglot_system/lib/`.
   - Compile the Go project to an executable named `go_encoder` located in `/home/user/polyglot_system/bin/`.

4. **Python Property-Based Testing (`/home/user/polyglot_system/verify.py`)**
   Write a Python script that uses the `hypothesis` library to perform property-based testing.
   - Use `hypothesis.strategies.text(min_size=1, max_size=100)` to generate random strings.
   - For each string, pass it to the Go executable via `subprocess`.
   - For each string, pass it to the Rust library using Python's `ctypes` module. (Assume the output buffer provided to Rust will never need to exceed 512 bytes).
   - Assert that both the Go executable and the Rust library produce the exact same hex-encoded output.
   - Run the property-based test. If it passes without any assertion errors, write the exact string `"PROPERTY_TESTS_PASSED"` to `/home/user/polyglot_system/test_results.log`. 

Run your build script, run the Python verification script, and ensure `/home/user/polyglot_system/test_results.log` is created successfully.