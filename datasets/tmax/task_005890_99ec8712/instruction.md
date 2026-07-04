You are tasked with fixing a C library build and integrating it into a new Rust-based WebSocket service. 

We have a legacy C library located at `/home/user/libexpr` that evaluates prefix math expressions (e.g., `ADD 10 20`). We want to expose this evaluator as a WebSocket service using Rust. However, there are several issues:
1. The C code has a memory safety vulnerability (buffer overflow) that causes segmentation faults on malformed or overly long inputs.
2. The CMake build configuration is incomplete, and downstream Rust projects cannot find the shared library at link time or runtime.

Your objectives:

**Phase 1: Fix and Build the C Library**
1. Inspect `/home/user/libexpr/expr.c`. Find and fix the memory safety issue (specifically, a buffer overflow during string parsing). Ensure it safely parses operations without crashing on inputs up to 100 characters.
2. Update `/home/user/libexpr/CMakeLists.txt` if necessary and build the shared library (`libexpr.so`). Ensure the library is compiled and available in `/home/user/libexpr/build/`.

**Phase 2: Create the Rust WebSocket Server**
1. Initialize a new Rust project at `/home/user/ws_eval`.
2. Write a `build.rs` file to properly link against the `libexpr.so` library you built. You may need to set the correct `rpath` or link search paths so the resulting binary runs without requiring manual `LD_LIBRARY_PATH` modifications.
3. The C library exposes this function: `int evaluate_expression(const char* input, int* result);` (Returns 0 on success, -1 on failure). Create the appropriate FFI bindings in your Rust code.
4. Implement a WebSocket server in Rust (using the `tungstenite` or `tokio-tungstenite` crate) that listens on `127.0.0.1:9001`.
5. For every text message received over the WebSocket connection, pass the string to the C `evaluate_expression` function. 
    - If successful, send back the integer result as a string.
    - If it fails (returns -1), send back the string `"ERROR"`.

**Phase 3: Execution**
Compile your Rust project (`cargo build --release`).
Run the compiled Rust WebSocket server in the background. 
Write the PID of the running Rust server to `/home/user/server.pid`.

Make sure your server stays running so it can be tested. Ensure all paths used are absolute.