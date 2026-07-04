You are tasked with fixing a broken vendored Python package that relies on a C extension, and then exposing its functionality via a gRPC service. 

We have a vendored package located at `/app/vendored/pyfasthash`. It contains a highly optimized custom hashing algorithm implemented in C, wrapped for Python using the standard `ctypes` / C-extension mechanism. However, the package is currently broken due to a recent bad commit. 

Your objectives are:
1. **Fix the Vendored Package:** 
   - Inspect `/app/vendored/pyfasthash`.
   - The `setup.py` has a deliberate configuration error preventing it from compiling.
   - The `fasthash.c` file contains a corrupted inline assembly directive (or logical flaw injected recently) that causes a segmentation fault or illegal instruction when hashing. Analyze the C code, remove or fix the broken assembly/logic, and ensure the hashing algorithm properly iterates over the input string.
   - Successfully install the package in the local Python environment (e.g., `pip install /app/vendored/pyfasthash`).

2. **Implement a gRPC Service:**
   - Create a gRPC server in Python that utilizes the fixed `pyfasthash` module.
   - Save the following protobuf definition to `/home/user/service.proto` and compile it using `grpc_tools`:
     ```proto
     syntax = "proto3";
     package fasthash;

     service HashService {
       rpc ComputeHash (HashRequest) returns (HashResponse) {}
     }

     message HashRequest {
       repeated string items = 1;
     }

     message HashResponse {
       uint64 hash_value = 1;
     }
     ```
   - Write a server script at `/home/user/server.py`. 
   - The `ComputeHash` endpoint must concatenate all `items` from the request (in the order provided, without any delimiters) and pass the resulting byte string to the C extension's `compute_fast_hash` function.
   - The server must listen in plaintext on `127.0.0.1:50051`.
   - Start the server in the background so it is actively listening when you finish.

Write the code, compile the protobufs, fix the C extension, and run your gRPC server. Leave the server process running on `127.0.0.1:50051`.