You are an open-source maintainer reviewing a pull request for a new high-performance checksum validation microservice. A contributor has submitted a PR that adds a gRPC backend and an HTTP gateway, along with a vendored C library for fast CRC32 calculations. Unfortunately, the PR is broken and doesn't run.

Your task is to fix the project in `/app/workspace` so that both the gRPC service and HTTP gateway function correctly.

The project structure is:
`/app/workspace/`
  `vendored_crc/` - Contains the C source code and Makefile for the fast CRC library.
  `crc.proto` - Protobuf definition for the gRPC service.
  `server.py` - gRPC server implementation.
  `gateway.py` - HTTP server acting as a gateway.

Here are the specific issues you need to resolve:
1. **Vendored Package Build**: The `Makefile` inside `/app/workspace/vendored_crc` is broken (the contributor accidentally committed a test configuration). Fix the Makefile so that running `make` successfully compiles `libfastcrc.so`.
2. **gRPC and Protobuf**: The `crc.proto` file defines a service `ChecksumService` with a `Verify` RPC. However, the protobuf definition has a syntax error, and `server.py` has a mismatch with the generated code. Fix the proto file, generate the Python gRPC stubs (`grpc_tools.protoc`), and fix `server.py` so it properly loads `../vendored_crc/libfastcrc.so` and implements the RPC. The RPC should take a string `data` and an int32 `expected_crc`, and return a boolean `is_valid`.
3. **HTTP Gateway (URL Routing)**: `gateway.py` is an HTTP server that should expose a `GET /verify` endpoint. It needs to parse the query parameters `data` and `crc`. It must then make a gRPC call to the backend. Fix the routing and parameter parsing logic so it correctly extracts these parameters (where `crc` is parsed as an integer), calls the gRPC backend, and returns a JSON response: `{"valid": true}` or `{"valid": false}`. Return a 400 Bad Request if parameters are missing.

Requirements:
- The gRPC server must listen on `127.0.0.1:50051`.
- The HTTP gateway must listen on `127.0.0.1:8080` and connect to the gRPC server.
- Start both services in the background. Leave them running so they can be verified.
- Do not modify the C source code (`fastcrc.c`), only the Makefile.

Start the services using:
```bash
python3 server.py &
python3 gateway.py &
```
Ensure they are fully operational and listening on their respective ports.