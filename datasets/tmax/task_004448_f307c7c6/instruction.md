You are tasked with fixing a broken Rust library, integrating it into a gRPC service using Python, and writing a Bash script to interact with it.

Currently, there is a Rust project located at `/home/user/rust_lib`. It is intended to be built as a C-ABI shared library (`cdylib`) that calculates a simple 16-bit checksum (sum of bytes modulo 65536) for error-correcting purposes. However, the Rust project currently fails to compile because the function signature does not properly expose a C-ABI.

Your task consists of the following phases:

1. **Fix the Rust Library:**
   - Navigate to `/home/user/rust_lib`.
   - Modify `src/lib.rs` so that it exports a C-compatible function named `compute_checksum`. It must take a raw byte pointer (`*const u8`) and a length (`usize`), and return a `u16`. 
   - Ensure the function is not mangled (`#[no_mangle]`).
   - Build the library in release mode. The output should be a shared library (e.g., `target/release/librust_lib.so`).

2. **Define the gRPC Service:**
   - Create a Protocol Buffers file at `/home/user/grpc/service.proto`.
   - It must use `syntax = "proto3";` and package `checksum`.
   - Define a service `ChecksumService` with a single RPC method `Calculate`.
   - The RPC should take a `PayloadRequest` containing a single field `bytes data = 1;`.
   - The RPC should return a `ChecksumResponse` containing a single field `uint32 checksum = 1;`.

3. **Implement the Python gRPC Server:**
   - Generate the gRPC Python stubs from `service.proto` into `/home/user/grpc/`.
   - Write a Python server script at `/home/user/grpc/server.py`.
   - The server must load the compiled Rust shared library using Python's `ctypes` module.
   - Implement the `ChecksumService`. In the `Calculate` method, pass the incoming `data` bytes to the Rust `compute_checksum` function, and return the result.
   - The server must listen on `localhost:50051` and run indefinitely. Keep it running in the background for the next step.

4. **Write the Bash Client Script:**
   - Create an executable Bash script at `/home/user/run_client.sh`.
   - The script must accept exactly one argument: the path to a file.
   - The script must read the contents of the provided file and send it as the `data` payload to the gRPC service at `localhost:50051`.
   - You may write a tiny inline Python script inside the Bash script to make the gRPC call, or use `grpcurl` if you prefer.
   - The Bash script must output *only* the numeric checksum to standard output.

Once you have completed all steps, leave the gRPC server running in the background on port `50051` and ensure `/home/user/run_client.sh` works correctly.