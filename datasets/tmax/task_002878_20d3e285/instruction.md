You are a developer tasked with fixing a multi-file Rust project that builds a Web Security proxy for intercepting gRPC communications over WebSockets. The project currently fails to compile due to a combination of strict compiler flags catching memory safety issues in a C FFI library, and an outdated protobuf schema.

The project is located at `/home/user/ws_grpc_proxy`. 

Here is what is currently wrong:
1. **C/C++ Memory Safety:** The Rust project links against a C library located at `/home/user/ws_grpc_proxy/c_ext/validator.c`. The `build.rs` file compiles this C code with `-Werror=stringop-overflow` enabled. The function `validate_token(const char* input)` uses a vulnerable `strcpy(buf, input);` into a 32-byte buffer. This causes the compilation to fail.
2. **gRPC/Protobuf:** The protobuf definition at `/home/user/ws_grpc_proxy/proto/service.proto` is using `syntax = "proto2";`, but the Rust `tonic` / `prost` build requires `syntax = "proto3";`.

Your task is to write a single Bash script at `/home/user/fix_and_test.sh` that completely automates the repair, build, and verification process. 

The Bash script must perform the following actions sequentially:
1. **Patch the C file:** Use `sed` (or another bash tool) to replace the unsafe `strcpy(buf, input);` in `/home/user/ws_grpc_proxy/c_ext/validator.c` with a safe memory operation: `strncpy(buf, input, 31); buf[31] = '\0';`.
2. **Patch the Protobuf file:** Use `sed` to change `syntax = "proto2";` to `syntax = "proto3";` in `/home/user/ws_grpc_proxy/proto/service.proto`.
3. **Build the project:** Run `cargo build` inside the `/home/user/ws_grpc_proxy` directory.
4. **Start the server:** Run the built Rust binary (`cargo run` or executing `./target/debug/ws_grpc_proxy`) in the background. The server binds to `127.0.0.1:8080`.
5. **Wait for startup:** Add a short bash `sleep` to ensure the server starts.
6. **Test the WebSocket:** Use `curl` to perform a WebSocket upgrade request to the proxy to verify it is running. Send a request to `http://127.0.0.1:8080/ws`. You must include standard WebSocket headers (e.g., `Connection: Upgrade`, `Upgrade: websocket`, `Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==`, `Sec-WebSocket-Version: 13`).
7. **Log the Output:** Capture the HTTP response headers from the `curl` command and save them to `/home/user/ws_test.log`.

Make sure your script is executable (`chmod +x`). Do not manually fix the files; your script `/home/user/fix_and_test.sh` must do it all.