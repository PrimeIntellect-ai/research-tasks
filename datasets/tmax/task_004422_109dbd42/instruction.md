You are a systems programmer working on a backend data processing pipeline. We have a Python gRPC service that uses a C shared library via `ctypes` for high-performance string parsing. 

Currently, the service is failing due to a mix of memory safety issues in the C library and missing functionality in the Python gRPC server. 

Here is what you need to do:

1. **Fix the C Library Memory Issue**: 
   The C code located at `/home/user/src/processor.c` implements a state machine parser that extracts alphanumeric tokens from a string. However, it crashes with a segmentation fault when processing inputs with too many tokens. Identify the memory safety vulnerability (array out-of-bounds / undefined behavior) and fix it so it safely truncates or ignores tokens that exceed the maximum limit defined in the code. Recompile it as a shared library `libprocessor.so` in `/home/user/src/`.

2. **Fix the Python Linking Issue**:
   The Python server at `/home/user/src/server.py` attempts to load `libprocessor.so` but is accidentally hardcoded to load an old, broken system library `/usr/lib/libprocessor.so`. Modify `server.py` to correctly load the newly compiled library from `/home/user/src/libprocessor.so`.

3. **Implement the Missing gRPC Endpoint**:
   The gRPC service defines a `GetTokenDiff` RPC in `/home/user/src/service.proto`. 
   In `/home/user/src/server.py`, implement this method. It receives two strings (`input_a` and `input_b`). It must:
   - Parse both strings using the C library's `extract_tokens` function.
   - Sort both lists of extracted tokens lexicographically.
   - Compute the symmetric difference (tokens present in A or B, but not both).
   - Return the result as a list of strings in the `tokens` field of the gRPC response, sorted lexicographically.

4. **Verify and Generate the Output Log**:
   Once the server is fixed and running, execute the provided test client `/home/user/src/client.py`. It will call the `GetTokenDiff` endpoint with a specific test payload and write the results to `/home/user/diff_result.txt`.

Ensure your fixes are robust and the resulting file `/home/user/diff_result.txt` exactly matches the expected symmetric difference output.