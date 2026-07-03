You are tasked with setting up a polyglot test harness and fixing a memory bug in a mixed C/Python microservice. The service calculates specialized values via a C shared library but communicates via a Python gRPC interface.

You will find the source code in `/home/user/polyglot_service/`.
Here is what you need to do:

1. **gRPC Setup**: 
   Compile the protocol buffer file `/home/user/polyglot_service/math_ops.proto` to generate the required Python gRPC stubs in the same directory.
   
2. **Shared Library Management & Memory Debugging**: 
   The service relies on a C library at `/home/user/polyglot_service/libmath.c`. 
   Compile this C file into a shared library named `libmath.so` in the same directory. 
   There is a known memory leak in `libmath.c`. Identify and fix the memory leak in `libmath.c`, then recompile the shared library.

3. **Constraint Satisfaction**:
   Create a test client script at `/home/user/polyglot_service/test_client.py`. Your script must programmatically find two integers `x` and `y` that satisfy the following constraints:
   - `x + y == 120`
   - `x * y == 3456`
   - `x > y`
   *(Hint: You can use a constraint solver like `z3-solver` or write a brute-force search)*.

4. **Integration Testing**:
   Your `test_client.py` must send the solved `x` and `y` values to the gRPC server defined in `server.py` using the `ComputeMagic` RPC call.
   Start the server in the background, run your client, and let the server process the request. The server is pre-configured to write the final successful computation to `/home/user/result.json`.

Make sure to install any required Python packages (e.g., `grpcio`, `grpcio-tools`, `z3-solver`) in your user environment. Do not use sudo.
The task is complete when `/home/user/result.json` is correctly written by the server and `libmath.c` is leak-free.