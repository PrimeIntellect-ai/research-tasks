You are a web developer working on a new microservices feature. Our project uses gRPC and Protocol Buffers. Recently, a team member updated our proto definitions, but they introduced a dependency conflict similar to a mismatched peer dependency in Node.js: one of the proto files imports a version of a common types file that doesn't exist, breaking the build.

Your task is to identify the broken dependency, patch it, compile the polyglot proto files for Python, and write an integration test.

Follow these exact steps:

1. **Dependency Resolution**:
   Our protobuf files are located in `/home/user/proto_deps`. 
   Write a Python script (or use bash tools) to parse all `.proto` files recursively, build a dependency graph of the `import` statements, and find the single imported `.proto` file path that does *not* exist on the filesystem. 
   Write the exact relative path of this missing import (e.g., `foo/v3/bar.proto`) to `/home/user/missing_dep.txt`.

2. **Patch Processing**:
   I have provided a patch file at `/home/user/fix_imports.patch` that corrects the faulty import. 
   Apply this patch to the `proto_deps` directory.

3. **Polyglot Build Orchestration**:
   Create a directory `/home/user/gen`.
   Compile all the `.proto` files in `/home/user/proto_deps` into Python gRPC files inside `/home/user/gen`. You must use `grpcio-tools` (which you can install or run via `python -m grpc_tools.protoc`). Make sure to set the import path (`-I`) correctly so the proto files can find each other.

4. **gRPC Test Creation**:
   Write a Python test script at `/home/user/test_gateway.py`. This script must:
   - Add `/home/user/gen` to the Python path so the generated modules can be imported.
   - Import the generated classes for the `Gateway` service (defined in `api/v1/gateway.proto`).
   - Implement a dummy server for `GatewayServicer` that responds to the `GetUserToken` RPC. If the incoming `UserRequest` has `user_id` set to `"test_user"`, the server should return a `TokenResponse` with `token` set to `"granted_token_123"`.
   - Start the gRPC server locally on port `50051`.
   - Create a local insecure gRPC channel and a stub to connect to `localhost:50051`.
   - Send a `UserRequest` with `user_id="test_user"` to the server.
   - Assert that the response token is `"granted_token_123"`.
   - If the assertion passes, write the exact string `TEST_PASSED` to `/home/user/test_result.log` and exit gracefully.

Run your test script to generate the log file.