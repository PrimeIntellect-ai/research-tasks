You are a build engineer for a web security company. You are managing a polyglot repository that generates highly optimized checksums for web session tokens. 

The workspace is located at `/home/user/workspace`. Inside, you will find two subdirectories:
1. `rust_part/`: A Rust project intended to build a shared library `librust_part.so`. It exposes a C ABI function `rust_checksum(const char* data)` which returns a 32-bit unsigned integer. Currently, the Rust project fails to compile due to a lifetime error in `src/lib.rs`.
2. `c_part/`: A C project containing `c_checksum.c` and a `Makefile`. It builds a shared library `libcchecksum.so` that exposes `c_checksum(const char* data)`. The `Makefile` is broken and fails to produce a valid shared object because of missing compiler flags for position-independent code.

Your tasks are:
1. Fix the Rust lifetime compilation error in `/home/user/workspace/rust_part/src/lib.rs`.
2. Fix the `Makefile` in `/home/user/workspace/c_part/Makefile` so it correctly compiles the shared library.
3. Build the Rust project (using `cargo build --release`) and the C project (using `make`).
4. Write a Python script at `/home/user/workspace/verify_token.py` that uses the `ctypes` module to load both shared libraries.
5. In your Python script, pass the string `"admin=true&user=alice"` to both the Rust and C checksum functions.
6. The Python script must output the exact results to a log file located at `/home/user/workspace/build_artifacts.log` in the following format:
```
Rust Checksum: <value>
C Checksum: <value>
```

Ensure your Python script runs successfully and generates the log file correctly.