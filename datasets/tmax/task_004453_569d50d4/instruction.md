I am reviewing a Pull Request for our open-source gRPC-to-WebSocket proxy project, but the contributor's PR is currently failing our integration tests. 

The PR does two things:
1. Migrates our protobuf schema (`service.proto`) to add a new `string client_version = 2;` field.
2. Updates the WebSocket proxy server (`ws_server.py`) to drop any requests where the `client_version` is older than `2.2.0`.

However, the contributor made two critical mistakes:
1. They updated the `service.proto` file but forgot to compile it to regenerate the Python gRPC stubs.
2. They used a naive Python string comparison to check the semantic version (e.g., `if request.client_version >= "2.2.0":`). This logic is broken because a semantic version like `"2.10.0"` evaluates as less than `"2.2.0"` in a naive string comparison.

Your task is to fix this PR:
1. Navigate to `/home/user/project`.
2. Compile the `service.proto` file to generate the corresponding Python files (`service_pb2.py` and `service_pb2_grpc.py`). You can use the `grpc_tools.protoc` module for this.
3. Fix the version comparison logic in `/home/user/project/ws_server.py`. You should use a robust semantic versioning comparison (e.g., the `Version` class from the `packaging.version` module) to properly compare `request.client_version` against the minimum required version of `"2.2.0"`.
4. Run the proxy server (`python ws_server.py &`) in the background.
5. Run the provided test script (`python test_client.py`).

The server is designed to write its outcomes to `/home/user/project/proxy_results.log`. For requests meeting the minimum version (like `"2.10.0"`), it should log `SUCCESS: Forwarded message to WS`. For older versions (like `"2.1.0"`), it should log `REJECTED: Version too low`.

Please correct the project so that running `test_client.py` successfully populates the log file with the correct accept/reject decisions.