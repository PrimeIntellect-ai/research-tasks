You are a developer jumping into a broken Python project that acts as a gRPC-based log parser and state machine. The project is located in `/home/user/grpc_state_service`.

Currently, the service fails to start or process requests correctly due to a few issues:
1. **gRPC/Protobuf missing field**: The client script (`client_test.py`) expects to send a `sequence_number` in the `ParseRequest` message, and the server (`server.py`) tries to read it, but it is missing from `service.proto`.
2. **Semantic Versioning Bug**: The server only accepts connections from clients with version >= "1.9.0". However, it currently uses simple string comparison, which incorrectly rejects version "1.10.0" sent by the client. You need to implement a proper semantic version comparison in `server.py` that handles major, minor, and patch numbers.
3. **State Machine Bug**: The parser uses a simple state machine. When it is in the `RUNNING` state, the event `HALT` should transition it to `STOPPED`. There is a typo or logic error in the transition table in `server.py` preventing this.

Your task:
1. Fix `service.proto` by adding `int32 sequence_number = 3;` to the `ParseRequest` message.
2. Regenerate the Python protobuf files (`service_pb2.py` and `service_pb2_grpc.py`) using `grpc_tools.protoc`.
3. Fix the semantic version check logic in `server.py`.
4. Fix the state machine transition in `server.py`.
5. Run the provided `/home/user/grpc_state_service/client_test.py` script.

If everything is fixed, `client_test.py` will automatically benchmark the server, perform serialization/deserialization checks, and generate a validation file at `/home/user/test_result.json`.

The automated test will verify the task by checking if `/home/user/test_result.json` exists and contains the expected success parameters.