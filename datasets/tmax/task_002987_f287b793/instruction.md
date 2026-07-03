You are tasked with replacing a legacy web security authentication microservice. 

The current codebase is a multi-file Rust project located in `/home/user/rust_auth`. Unfortunately, following a botched library update, the Rust project fails to compile. We cannot fix the Rust code right now. However, we do have an older compiled, stripped binary of this service located at `/app/legacy_auth`. This binary is known to suffer from memory leaks, but its cryptographic logic is correct.

Your task is to completely rewrite this service in Python 3.

**Requirements:**
1. **gRPC Protocol Setup:** 
   The broken Rust project contains the service definitions. Find the protobuf file in `/home/user/rust_auth/proto/` and use it to compile the Python gRPC stubs. The service implements an `AuthService` with a `GenerateToken` RPC.

2. **Reverse Engineering the Oracle:**
   The legacy stripped binary `/app/legacy_auth` is an executable that, when run, listens for gRPC requests on `127.0.0.1:50050`. 
   Analyze this binary (using `strings`, `objdump`, or treating it as a black-box oracle) to determine the exact token generation algorithm and the hardcoded secret key it uses. The algorithm generates a secure signature based on the user ID and payload.

3. **Python Implementation:**
   Create a new Python gRPC server in `/home/user/server.py`. 
   - It must implement the exact same `AuthService` behavior as the legacy binary.
   - It must bind to `127.0.0.1:50051`.
   - It must run continuously when executed via `python3 /home/user/server.py`.

4. **Integration Testing and Memory Profiling:**
   Write a comprehensive test suite in `/home/user/test_auth.py` using `pytest`. The test must:
   - Connect to the Python server on port 50051.
   - Send 100 randomly generated requests.
   - Connect to the legacy oracle on port 50050, send the exact same 100 requests, and assert that the generated tokens match perfectly.
   - Use Python's `tracemalloc` library to profile the memory usage of the gRPC client/server interaction during these 100 requests. Assert that the peak memory usage during the test loop does not exceed 5MB.

**Deliverables:**
- The compiled Python protobuf files.
- `/home/user/server.py` (your Python gRPC server).
- `/home/user/test_auth.py` (your pytest and memory profiling script).

Leave your `server.py` functioning so it can be automatically tested. The automated verification system will start your server and send real gRPC requests to `127.0.0.1:50051` to verify correct protocol implementation, cryptographic accuracy, and successful compilation of the stubs.