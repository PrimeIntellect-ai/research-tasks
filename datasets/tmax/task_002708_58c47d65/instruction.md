You are an integration developer modernizing a legacy mathematical system. We have a highly optimized (legacy) C library that calculates a proprietary mathematical transformation, and we need to expose it over a gRPC API using Rust to evaluate its performance overhead.

Your task is to implement the gRPC server in Rust, bind to the legacy C library via FFI, and write a benchmark script to test it.

**Setup Information:**
The legacy C library is located at `/home/user/legacy_math/`. 
It contains:
- `math_core.h`: Declares the function `uint64_t compute_transform(uint64_t input);`
- `libmath_core.so`: The compiled shared library.

A skeleton Rust project has been initialized at `/home/user/grpc_service/`. The `Cargo.toml` already includes dependencies for `tonic`, `prost`, and `tokio`.

**Requirements:**

1. **Protobuf Definition:**
   Create a protobuf file at `/home/user/grpc_service/proto/transform.proto`.
   - Package name: `transform_api`
   - Service name: `TransformService`
   - RPC: `ApplyTransform` taking a `TransformRequest` and returning a `TransformResponse`.
   - `TransformRequest` must have a single `uint64 value` field (tag 1).
   - `TransformResponse` must have a single `uint64 result` field (tag 1).

2. **FFI and Server Implementation:**
   Implement the gRPC server in Rust within `/home/user/grpc_service/`.
   - You will need to write a `build.rs` to compile the protobuf and link the C library `math_core`.
   - In `src/main.rs`, declare the FFI binding to `compute_transform`.
   - Implement the `TransformService` using `tonic`. The `ApplyTransform` endpoint should call the C function via FFI with the requested value and return the result.
   - The server must listen on `127.0.0.1:50051`.
   - Compile the server (`cargo build --release`).
   - Run the server in the background. Note: you may need to set `LD_LIBRARY_PATH=/home/user/legacy_math` so the binary can find the `.so` file.

3. **Benchmarking Script:**
   Write a bash script at `/home/user/benchmark.sh` that acts as a simple integration test and benchmark.
   - The script must use `grpcurl` (which is installed on the system) to call the `ApplyTransform` endpoint on `127.0.0.1:50051` in plaintext (`-plaintext`).
   - Request the transform for the input value `1337`.
   - Extract the `result` from the JSON response and save *only the numeric result* to `/home/user/answer.txt`.
   - Next, to benchmark, the script should invoke `grpcurl` 50 times in a loop with input `1000`, measuring the total time taken for the loop (using the `time` command or `date` differences), and append the time in seconds to `/home/user/benchmark_result.txt`.

Ensure your server is running and your `benchmark.sh` has been executed successfully before concluding the task.