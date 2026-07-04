You are tasked with fixing a build and testing pipeline for a multi-file Rust project located in `/home/user/project`. 

The project is a WebSocket server written in Rust that processes a custom data structure. It offloads the heavy processing to a C library via FFI. The project currently fails to compile for our edge devices (`aarch64-unknown-linux-gnu`) because the provided Bash build script (`/home/user/project/build.sh`) incorrectly compiles the C FFI dependency using the host compiler instead of the cross-compiler, and fails to link it.

Your objective is to:
1. Fix the `/home/user/project/build.sh` script so that it properly cross-compiles the C library (`src/c_src/processor.c`) into a static archive (`libprocessor.a`) for the `aarch64-unknown-linux-gnu` target. You must use the standard `aarch64-linux-gnu-gcc` and `aarch64-linux-gnu-ar` tools.
2. Ensure the script configures Cargo to use the correct linker for the `aarch64` target by generating a `.cargo/config.toml` file within the project directory.
3. Once the build script is fixed, write a Bash testing script at `/home/user/project/test_ws.sh`. This script should:
   - Assume the compiled `x86_64` version of the server is running locally on port `8080`.
   - Act as a minimal WebSocket client using standard Bash tools (e.g., `curl` with protocol upgrade headers).
   - Send a custom JSON data structure: `{"command": "process", "payload": [1, 2, 3, 4]}` to the WebSocket endpoint `ws://localhost:8080/stream`.
   - Capture the HTTP/WebSocket response headers and body, saving the raw output strictly to `/home/user/ws_test_output.log`.

Constraints:
- Do not modify the Rust (`*.rs`) or C (`*.c`) source files.
- You must write the test script using only standard Bash shell tools (like `curl`, `printf`, `nc`, etc.). Do not write a custom Python/Node client.
- Ensure `test_ws.sh` is executable.
- Your build script must exit with `0` on success.