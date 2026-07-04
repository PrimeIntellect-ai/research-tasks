I'm working on a high-performance data processing pipeline in `/home/user/data_pipeline` that uses a custom C library (for a fast string hash set) wrapped by a Rust application. 

However, I'm running into a few issues that I need you to fix:

1. **Build and Linking Issues:** The Makefile in `/home/user/data_pipeline/c_lib` doesn't properly generate a static library (`libfilter.a`), and the Rust project's `build.rs` isn't correctly configured to link against it. When I run `cargo build` in `/home/user/data_pipeline/rust_app`, it fails to link the C functions.
2. **Rust Lifetime Issue:** Even if you force it to link, `src/main.rs` has a severe lifetime issue. It uses `std::ffi::CString::new(string).unwrap().as_ptr()` inline when calling the C FFI, which causes the `CString` to be dropped prematurely, leading to dangling pointers and memory corruption (or constraint failures). You need to fix `src/main.rs` so that the `CString` lives long enough for the FFI call.
3. **End-to-End Orchestration & Benchmarking:** Once the program is fixed and builds successfully via `cargo build --release`, write a shell script at `/home/user/run_pipeline.sh`. This script must:
   - Read lines from `/home/user/data.txt`
   - Pass the file path `/home/user/data.txt` as the first argument to the compiled Rust binary (`/home/user/data_pipeline/rust_app/target/release/rust_app`).
   - Pipe the standard output of the Rust binary to `/home/user/results.txt`.
   - Measure the execution time of the Rust binary using the `time -p` command.
   - Extract ONLY the "real" time value (in seconds, e.g., `0.05`) and write it to `/home/user/bench_log.txt`.

**Expected System State:**
- The Makefile correctly produces `libfilter.a`.
- `build.rs` correctly specifies the library search path and static library name.
- `main.rs` compiles without warnings and correctly preserves the lifetimes of strings passed to C.
- `/home/user/results.txt` contains exactly the output of the Rust binary.
- `/home/user/bench_log.txt` contains a single floating-point number representing the real execution time in seconds.