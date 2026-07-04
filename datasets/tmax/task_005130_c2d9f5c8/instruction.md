You are a platform engineer responsible for maintaining our CI/CD pipeline infrastructure. A recent update broke our internal Dependency Resolver microservice. Your goal is to fix the build, recreate the missing service definitions, and orchestrate the service startup using Bash.

Here is what you need to do:

1. **Extract Authentication Requirements:**
   There is an architecture diagram at `/app/pipeline_specs.png`. This image contains a note with the required CI authentication token (formatted as `TOKEN: <value>`). You must extract this token (e.g., using `tesseract`) as it is required to start the service securely.

2. **Fix the C Project Build:**
   Our core dependency graph traversal and semantic version comparison logic is written in C, located in `/app/dep_resolver/`. The `Makefile` has a linking error and currently fails to build the shared library `libresolver.so`. You must fix the `Makefile` (hint: it might be missing a flag to link the math library, or the object file order is wrong).

3. **Design the Protobuf Service:**
   The original `.proto` file was accidentally deleted. Create a new file at `/app/proto/resolver.proto` with `syntax = "proto3";` and package `ci`.
   Define a service named `DependencyResolver` with a single RPC method:
   `rpc ResolveGraph (ResolveRequest) returns (ResolveResponse);`
   - `ResolveRequest` must have two fields: `string package_name = 1;` and `string current_version = 2;`
   - `ResolveResponse` must have two fields: `bool is_valid = 1;` and `string resolved_tree = 2;`

4. **Test Orchestration (Bash):**
   Write a Bash script at `/app/run_service.sh` that does the following:
   - Compiles the C library by running `make -C /app/dep_resolver/`.
   - Generates the Python gRPC stubs for `resolver.proto` in `/app/` (using `python3 -m grpc_tools.protoc`).
   - Exports the extracted token as an environment variable named `GRPC_AUTH_TOKEN`.
   - Starts the pre-existing server script `/app/server.py` in the background. The server is configured to listen on port `50505`.

Ensure your Bash script has executable permissions. Once you have completed these steps, execute `/app/run_service.sh` and leave the server running so our automated test suite can verify the gRPC endpoint.