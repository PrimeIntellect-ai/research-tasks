You are a mobile build engineer maintaining an automated testing pipeline. Recently, our metadata extraction service has been failing during the pipeline integration tests. 

Your objective is to fix the underlying memory bug in our C-extension, and then write a Python testing script that integrates gRPC, WebSockets, and Semantic Versioning to verify the build pipeline.

Here is the setup in your workspace (`/home/user`):

1. **The Metadata Extractor (C Library):**
   We have a C library at `/home/user/extractor.c` that parses version strings. It is currently causing the build service to crash (segfault) when it receives long inputs.
   - Fix the memory safety issue (undefined behavior/buffer overflow) in `extractor.c`. 
   - Recompile it as a shared library: `gcc -shared -o libextractor.so -fPIC extractor.c`

2. **The gRPC Service:**
   We have a gRPC service defined in `/home/user/build_service.proto` and implemented in `/home/user/grpc_server.py`. It loads `libextractor.so` using `ctypes`. 
   - Once the C library is fixed and recompiled, start the gRPC server in the background: `python3 grpc_server.py` (runs on `localhost:50051`).

3. **The Event Server (WebSocket):**
   There is a mock build event server running at `ws://localhost:8080`. When you connect to it, it immediately sends a single JSON message containing a list of release candidates:
   `{"candidates": ["1.0.0", "2.1.0-alpha", "1.5.2", "2.0.1", "1.5.11"]}`

4. **Your Task - The Pipeline Test Script:**
   Write a Python script at `/home/user/pipeline_test.py` that does the following:
   - Connects to the WebSocket server at `ws://localhost:8080` and retrieves the JSON payload.
   - Parses the versions and uses strict Semantic Versioning (SemVer 2.0.0) comparison to find the **highest stable version**. (Ignore any pre-release versions like `-alpha`, `-beta`, etc.).
   - Connects to the gRPC service at `localhost:50051` using the stub generated from `build_service.proto`.
   - Calls the `ValidateRelease` RPC endpoint, passing the highest stable version string as the `version_payload`.
   - The gRPC service will return a validation code (string).
   - Write this exact validation code string to a file at `/home/user/pipeline_result.log`.

**Constraints:**
- Do not use root/sudo. 
- You may install standard Python packages via pip (e.g., `grpcio`, `grpcio-tools`, `websockets`, `packaging` or `semantic_version`).
- Ensure your script generates the protobuf Python bindings from `build_service.proto` before running.
- To succeed, `/home/user/pipeline_result.log` must contain exactly the validation string returned by the gRPC service.