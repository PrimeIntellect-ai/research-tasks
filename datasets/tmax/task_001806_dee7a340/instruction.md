You are tasked with upgrading a data processing pipeline as part of a migration from a legacy Python 2 client to a modern Python 3 client. The backend is a C++ gRPC service that performs data calculations.

Currently, the C++ service has a known memory leak and an outdated protobuf schema. You need to update the schema, fix the backend, and write a new Python 3 benchmarking client.

The existing files are located in `/home/user/`:
- `/home/user/backend/data_service.proto`: The protobuf schema.
- `/home/user/backend/server.cpp`: The C++ gRPC server implementation.
- `/home/user/backend/CMakeLists.txt`: CMake build instructions.
- `/home/user/client/client_v2.py`: The legacy Python 2 client (for reference only, you don't need to run it).

Here are your objectives:

1. **Update Protobuf Schema**: 
   Modify `/home/user/backend/data_service.proto` to add a new field to the `DataPoint` message: `double weight = 3;`.

2. **Fix and Update C++ Backend**:
   - Update `/home/user/backend/server.cpp` to use the new `weight` field. The `processed_value` in the `DataResult` should be calculated as `request->value() * request->weight()`.
   - There is a memory leak in the `ProcessData` method of `server.cpp`. Identify and fix this memory leak. 

3. **Build the C++ Server**:
   Compile the C++ server in `/home/user/backend/build/`. The output executable should be named `server`.

4. **Write Python 3 Client and Benchmark**:
   Create a Python 3 client at `/home/user/client/client_v3.py` that does the following:
   - Connects to the gRPC server at `localhost:50051`.
   - Generates the necessary Python gRPC stubs from the updated `.proto` file (you can do this via command line or within the script).
   - Sends 1000 `ProcessData` requests sequentially. For each request, set `id` from 1 to 1000, `value` to `10.0`, and `weight` to `2.5`.
   - Measures the total time taken to complete all 1000 requests to calculate the average latency per request in milliseconds.
   - Verifies that all 1000 responses have a `processed_value` of exactly `25.0`.
   - Writes the benchmark results to `/home/user/benchmark.log` with exactly the following two lines:
     `All values correct: True` (or False if they are not)
     `Average latency: X.XX ms` (where X.XX is the calculated average latency).

Ensure that your compiled C++ server runs without any memory leaks. You are encouraged to use `valgrind` to verify this.

System requirements:
- C++ gRPC and Protobuf libraries are already installed via `apt` (e.g., `libgrpc++-dev`, `protobuf-compiler-grpc`).
- `grpcio` and `grpcio-tools` for Python 3 are installed.