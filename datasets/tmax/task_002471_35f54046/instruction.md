You are a web developer building a high-performance backend feature: a gRPC metadata processing service written in Python that delegates heavy text processing to a C++ shared library. 

Your repository is located at `/home/user/project/`. 

Currently, the project is broken. The C++ library has a memory safety issue that causes the server to crash on large inputs, the build system is incomplete, and the gRPC service lacks the required rate limiting.

Your objectives:

1. **Fix the Build System (`/home/user/project/Makefile`)**
   - The Makefile should compile `cpp/processor.cpp` into a shared library named `libprocessor.so` in the `build/` directory. Ensure the correct compiler flags are used to create a shared object.
   - It must also compile the protobuf file `proto/metadata.proto` into Python gRPC code (place the generated `_pb2.py` and `_pb2_grpc.py` files in the `python/` directory).
   - Add a `make all` target that performs both of these steps.

2. **Fix the C++ Memory Bug (`/home/user/project/cpp/processor.cpp`)**
   - The `process_data(const char* input, char* output)` function currently uses unsafe string copying, causing a segmentation fault when `input` exceeds a certain length. 
   - Fix the undefined behavior and memory vulnerability so it safely handles strings up to 1000 characters without crashing. The output buffer provided by the Python wrapper will always be 1024 bytes. The expected output format is exactly: `Processed: <input_string>`.

3. **Complete the Python gRPC Server (`/home/user/project/python/server.py`)**
   - Implement the `MetadataService` defined in `proto/metadata.proto`.
   - Use `ctypes` to load `../build/libprocessor.so` and call `process_data` to compute the result for the `data` field of the `ProcessRequest`.
   - **Rate Limiting:** Implement an in-memory rate limiter. A single `client_id` is only allowed to make **3 requests per second**. If a client exceeds this, the server must reject the request by raising a gRPC exception with the status code `grpc.StatusCode.RESOURCE_EXHAUSTED` and the exact detail message `"Rate limit exceeded"`.

4. **Deployment Script (`/home/user/project/start.sh`)**
   - Create a bash script at `/home/user/project/start.sh` that:
     - Runs `make all` to build all necessary artifacts.
     - Starts the Python gRPC server on port `50051` in the background.
     - Writes the PID of the server to `/home/user/project/server.pid`.
   - Ensure the script is executable.

Constraints:
- Do not use any external databases (e.g., Redis) for rate limiting; use standard Python data structures in memory.
- Use `python3` for your environment. You may install `grpcio` and `grpcio-tools` via pip if needed.