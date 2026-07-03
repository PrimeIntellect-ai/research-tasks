You are acting as a systems programmer. We have a multi-component system consisting of a highly optimized data processing library written in Rust, and a Python gRPC server that exposes this library to network clients. 

Currently, the system is broken and incomplete. You need to fix the library, write the gRPC server using Python and `ctypes`, and verify it works.

Here is the situation:
1. There is a Rust library located in `/home/user/project/rust_lib`. It is supposed to compile to a C dynamic library (`cdylib`). However, the original developer left a borrow checker bug in `/home/user/project/rust_lib/src/lib.rs`. 
2. The protobuf definition for the gRPC service is located at `/home/user/project/compute.proto`.
3. The Python gRPC server is missing.

Your tasks:
1. **Fix the Rust library:** Navigate to `/home/user/project/rust_lib` and fix the borrow checker error in `src/lib.rs`. The function `process_buffer` is exposed via FFI. It takes an input byte array, adds `0x05` to each byte, and writes the result to the output byte array. Do not change the function signature. Build the release version of the shared library.
2. **Compile Protobuf:** Generate the Python gRPC and protobuf bindings from `/home/user/project/compute.proto`. Put the generated files in `/home/user/project/`.
3. **Write the gRPC Server:** Create `/home/user/project/server.py`. It must:
   - Load the compiled Rust shared library (`libprocessor.so`) using Python's `ctypes`. Set the correct `argtypes` and `restype` for the FFI function.
   - Implement the `ComputeService` servicer.
   - For the `ProcessData` RPC, read the `payload` bytes from the request, allocate an appropriately sized output buffer, pass both to the Rust `process_buffer` FFI function, and return the mutated bytes in the `ProcessResponse`'s `result` field.
   - Start an insecure gRPC server on `localhost:50051`.
4. **Test the System:** Start your server in the background. Then, write and execute a client script at `/home/user/project/client.py`. The client must connect to the server at `localhost:50051`, send a `ProcessRequest` with the payload `b"SYSTEMS_PROGRAMMING"`, and receive the response. 
5. **Log the Output:** The client must write the hex-encoded string of the returned `result` bytes (e.g., using `.hex()`) to exactly `/home/user/project/output.log`.

Constraints:
- Do not modify `compute.proto`.
- You may install any Python packages you need (like `grpcio`, `grpcio-tools`) in your local user environment (`pip install --user`).