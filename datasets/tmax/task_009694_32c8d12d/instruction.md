You are a web developer building a high-performance data processing backend feature. To optimize a specific endpoint, you have decided to use a polyglot architecture: Python for the web logic and structured data parsing, Rust for string transformations, and a minimal C shared library for an assembly-level checksum operation. 

However, the current project is in an incomplete and broken state. Your task is to fix the codebase, complete the missing components, and create a local CI/CD build script to orchestrate the compilation and testing pipeline.

The project is located at `/home/user/app/`. 

Here is what you need to do:

1. **Fix the Rust Module (`/home/user/app/rust_transform/`)**:
   - The Rust crate is intended to be compiled into a C-compatible shared library (`librust_transform.so`).
   - The function `reverse_string` is exported via FFI, but the file `/home/user/app/rust_transform/src/lib.rs` has a lifetime compilation error. 
   - Fix the lifetime issue so the function takes a C-string, reverses it, and returns a freshly allocated C-string. 
   - Compile it to a release shared library (`cargo build --release`).

2. **Implement the Checksum Helper (`/home/user/app/asm_helper.c`)**:
   - Write a C function `uint8_t xor_checksum(const char *data, int len)` in this file. 
   - It must compute and return the byte-wise XOR of all characters in the string `data`.
   - Compile this file into a shared library named `libasm_helper.so` in `/home/user/app/`.

3. **Complete the Python Pipeline (`/home/user/app/main.py`)**:
   - Write a Python script that uses `json` and `ctypes`.
   - It should read `/home/user/app/input.json` (which contains an array of objects like `{"id": 1, "payload": "hello"}`).
   - For each object, load the payload. Pass it to the Rust `reverse_string` function (make sure to handle memory/pointers appropriately, though memory leaks are acceptable for this task).
   - Pass the reversed string to the C `xor_checksum` function.
   - Construct a new JSON array with objects containing: `{"id": 1, "reversed": "olleh", "checksum": <int>}`.
   - Write this array to `/home/user/app/result.json`.

4. **Orchestrate the Build (`/home/user/app/build_and_test.sh`)**:
   - Create a bash script that:
     a) Compiles the C library (`libasm_helper.so`).
     b) Builds the Rust project.
     c) Copies the Rust `librust_transform.so` from `target/release/` to `/home/user/app/`.
     d) Runs `python3 main.py`.
   - Make sure the script is executable and run it to produce the final `result.json`.

Ensure that running `/home/user/app/build_and_test.sh` cleanly executes all steps and generates `/home/user/app/result.json` successfully.