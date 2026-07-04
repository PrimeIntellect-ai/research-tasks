You are tasked with completing the migration of a legacy Python 2 application to Python 3. The application is a tiny Virtual Machine (VM) emulator that receives programs via gRPC and executes them. It is located at `/app/tiny_vm_grpc`.

The previous developer started the migration but left it in a broken state. You need to fix the bugs, regenerate the gRPC stubs, ensure all tests pass, and optimize the emulator's performance.

Here are your specific objectives:
1. **Fix Python 3 Incompatibilities:** The source code in `/app/tiny_vm_grpc/src/vm.py` and `/app/tiny_vm_grpc/src/utils.py` contains Python 2 idioms (such as `cmp()`, `xrange`, or `dict.has_key()`) that crash in Python 3. Update the code to be strictly Python 3 compatible.
2. **Fix Protocol Buffers:** The gRPC definitions are in `/app/tiny_vm_grpc/proto/vm_service.proto`. The generated Python files are missing or outdated. You need to use `grpc_tools.protoc` to generate `vm_service_pb2.py` and `vm_service_pb2_grpc.py` inside the `src/` directory so that `server.py` and `benchmark.py` can import them.
3. **Pass Unit Tests:** Ensure that running `pytest /app/tiny_vm_grpc/tests/test_vm.py` passes 100%. The tests will verify the correctness of the VM execution and the semantic version comparison utility.
4. **Optimize the Emulator:** The current VM implementation in `src/vm.py` is extremely inefficient, especially for loops, because it parses the raw program string repeatedly on every instruction step. You must refactor `vm.py` to pre-parse or tokenize the instructions before execution so it runs much faster. You must maintain exactly the same execution semantics.
5. **Run the Benchmark:** Once the tests pass and the server is running, execute `/app/tiny_vm_grpc/benchmark.py`. This script will start the gRPC server, send a computationally intensive program, measure the execution time, and write the duration (in seconds) to `/app/tiny_vm_grpc/benchmark_result.txt`.

**Success Criteria:**
- The file `/app/tiny_vm_grpc/benchmark_result.txt` must contain a single float value representing the execution time.
- The execution time must be strictly less than **0.5 seconds**.
- All unit tests must pass without any modifications to the test files.

Do not change the gRPC service definition or the `benchmark.py` script. Focus on fixing the source files, generating the stubs, and optimizing the emulator.