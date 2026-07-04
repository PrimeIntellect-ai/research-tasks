You are a build engineer responsible for migrating a legacy artifact management tool to a new architecture.

We are splitting the signature generation process into a gRPC-based service. The mathematical base calculation needs to be ported from legacy JavaScript to Python, and the final cryptographic permutation is handled by a high-performance Rust library.

Your task is to implement this system by following these steps:

1. **Protobuf Definition**: Create a protobuf file at `/home/user/proto/artifact.proto` using `proto3`. Define a package `artifact`. Create a service `ArtifactSigner` with an RPC method `Sign` that takes a `SignRequest` and returns a `SignResponse`. 
   - `SignRequest` should contain a single field: `bytes payload = 1;`
   - `SignResponse` should contain a single field: `uint64 signature = 1;`

2. **Rust Library Debugging & Linking**: 
   There is a Rust project at `/home/user/rust_lib`. It exposes a C-compatible function `process_signature(base: u64) -> u64`. However, it currently has a borrow checker error. 
   - Fix the ownership bug in `/home/user/rust_lib/src/lib.rs`. Do not change the mathematical operations, just fix the Rust compilation error.
   - Build the library in release mode. The resulting shared object will be at `/home/user/rust_lib/target/release/librust_lib.so`.

3. **Code Translation**: 
   We have a legacy JavaScript function at `/home/user/legacy/calc.js` that computes a base signature from a byte array. Translate this exact logic into Python. 

4. **Python gRPC Server**:
   Write a Python gRPC server in `/home/user/server/server.py`. 
   - Compile the protobufs for Python in the `/home/user/server` directory.
   - The server must listen on `[::]:50051`.
   - In the `Sign` implementation, first compute the base signature of the `payload` using your translated Python logic. 
   - Then, use the `ctypes` module to load `/home/user/rust_lib/target/release/librust_lib.so` and pass the base signature to the `process_signature` function.
   - Return the result in `SignResponse`.

5. **Python Client and Verification**:
   Write a script at `/home/user/client.py` that connects to your running server at `localhost:50051`.
   - Call the `Sign` method with the payload `b"artifact_v1_release"`.
   - Save the resulting integer signature as a plain text string to `/home/user/final_signature.txt`.

Ensure the server is running in the background before you execute your client script. You may install required Python packages like `grpcio` and `grpcio-tools` using `pip`.