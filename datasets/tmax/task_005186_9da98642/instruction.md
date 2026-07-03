You are a release manager preparing a new deployment for our core data processing microservice. The service wraps a high-performance C library using a Python gRPC server, and deployment metrics are reported to a dashboard via WebSockets. 

The latest release bundle is located in `/home/user/release`. However, the bundle is incomplete and has a known ABI mismatch bug due to a recent change in the C library's signature.

Your task is to fix the bundle, verify the service locally, and report the successful deployment check.

Please perform the following steps:
1. Navigate to `/home/user/release`. You will need to install `grpcio`, `grpcio-tools`, and `websockets` via pip.
2. Compile `processor.c` into a shared library named `libprocessor.so` in the same directory.
3. Generate the Python gRPC stubs from `data.proto`.
4. Fix the ABI mismatch in `grpc_server.py`. The C function `process_data` was recently updated to take a `double` and return a `double`, but the `ctypes` bindings in the Python server are still using integers.
5. Complete the deployment validation script `deploy_check.py`. It must:
   - Connect to the local gRPC server at `localhost:50051`.
   - Call the `Process` RPC with the value `4.0`.
   - Take the returned float value, format it as a string exactly like `SUCCESS: <value>` (e.g., `SUCCESS: 10.0`), and send it via WebSocket to `ws://localhost:8765`.
6. Start `ws_server.py` (runs the WebSocket server) and `grpc_server.py` (runs the gRPC server) in the background.
7. Run your completed `deploy_check.py`.

The task is considered successful when `/home/user/deploy_log.txt` is created by the WebSocket server and contains the correct formatted success message resulting from the value `4.0` being processed by the C library.