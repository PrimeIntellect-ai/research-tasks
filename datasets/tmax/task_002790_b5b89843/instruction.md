You are tasked with porting and modernizing a legacy system compatibility tool into a minimal containerized environment. As part of this, you need to build a new central Version Compatibility gRPC Daemon in Python, write the underlying semantic version comparison logic from scratch, and orchestrate the build and testing pipeline.

You need to perform the following steps:

1. **Protocol Design**: Create a Protocol Buffers file at `/home/user/compat/proto/compat.proto` with `syntax = "proto3";`.
   Define a service named `CompatibilityDaemon`. It must have an RPC method named `CheckVersion` that takes a `VersionRequest` and returns a `VersionResponse`.
   - `VersionRequest` must have two string fields: `component_name` (field 1) and `reported_version` (field 2).
   - `VersionResponse` must have a boolean field: `is_compatible` (field 1).

2. **Algorithmic Semver Logic**: In `/home/user/compat/server/semver.py`, implement a Python function `def evaluate_version(reported: str, constraint: str) -> bool:` that parses and compares strict Semantic Versions (MAJOR.MINOR.PATCH).
   - The `constraint` string will contain one or two conditions separated by a space (e.g., `>= 1.2.0`, `== 2.0.1`, `>= 1.0.0 <= 1.5.0`).
   - Supported operators are `>=`, `<=`, `==`.
   - You must parse the semantic versions from scratch (do not use external libraries like `semver` or `packaging`).
   - Return `True` if the reported version satisfies the constraint, `False` otherwise.

3. **gRPC Server Implementation**: In `/home/user/compat/server/main.py`, implement the gRPC server listening on port `50051`.
   - Use the generated protobuf code.
   - It should use the `evaluate_version` function to check compatibility against these hardcoded component constraints:
     - `frontend`: `>= 1.2.0 <= 1.5.0`
     - `backend`: `== 2.0.1`
     - `database`: `>= 14.0.0`
   - If a component is unknown, return `is_compatible = False`.

4. **Testing & Build Orchestration**: 
   - Write a pytest suite in `/home/user/compat/tests/test_semver.py` that thoroughly tests `evaluate_version`.
   - Create an orchestration bash script at `/home/user/compat/build_and_test.sh`. This script must:
     a) Install `grpcio`, `grpcio-tools`, and `pytest` using pip.
     b) Compile the protobuf file into Python code, placing the generated files in `/home/user/compat/server`.
     c) Run the pytest suite.
     d) Start the gRPC server in the background.
     e) Wait for the server to be ready.
     f) Create a Python client script on the fly to call the `CheckVersion` method with the following test cases, saving the boolean results (one per line, e.g., `True` or `False`) to `/home/user/compat/integration.log`.
        - Test 1: `frontend` with `1.4.2`
        - Test 2: `backend` with `2.0.0`
        - Test 3: `database` with `15.1.0`
     g) Kill the background server cleanly.

Make sure the bash script has executable permissions. Your final goal is to have the `build_and_test.sh` script execute flawlessly and produce `/home/user/compat/integration.log`.