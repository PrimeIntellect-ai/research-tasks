You are a mobile build engineer maintaining a CI/CD pipeline. A multi-file Rust project in the pipeline frequently fails to compile due to lifetime issues in a critical low-level component. To bypass this, we are creating a microservice that generates and serves a minimal native assembly shim to replace the failing component.

Your task is to build a Python-based gRPC service that parses a structured build manifest, extracts an assembly payload, compiles it into an executable ELF binary, and serves it to a client.

Follow these steps exactly:

1. **Protocol Definition**:
   Create a protobuf file at `/home/user/shim.proto`.
   It must define a package named `pipeline`.
   Define a service named `ShimBuilder`.
   Define an RPC named `BuildShim` that takes a `ShimRequest` and returns a `ShimResponse`.
   `ShimRequest` must contain a single string field `job_id` (tag 1).
   `ShimResponse` must contain a single bytes field `executable_payload` (tag 1).
   Compile this proto file for Python using `grpc_tools.protoc` into `/home/user/`.

2. **Data Parsing & Server Implementation**:
   Create a Python gRPC server at `/home/user/server.py` that listens on `[::]:50051`.
   The server must read the JSON file at `/home/user/build_manifest.json`.
   When `BuildShim` is called with a `job_id`, the server must:
   - Find the job with the matching `job_id` in the JSON array.
   - Extract the x86_64 assembly string from the `assembly_code` field.
   - Write this assembly to a temporary file, compile it into an object file using `nasm -f elf64`, and link it using `ld` to create a standalone executable.
   - Read the compiled executable's bytes and return them in the `ShimResponse`.

3. **Client Implementation**:
   Create a Python gRPC client at `/home/user/client.py`.
   The client must connect to the server at `localhost:50051`.
   It must send a `ShimRequest` with `job_id` set to `"rust-fallback-44"`.
   It must receive the `executable_payload`, write it to `/home/user/output_bin`, and ensure the file is executable (`chmod +x`).

To complete the task:
- Start the server in the background.
- Run the client so `/home/user/output_bin` is created.

Assume `nasm` and `binutils` (for `ld`) are already installed. You may install required Python packages like `grpcio` and `grpcio-tools` via pip.