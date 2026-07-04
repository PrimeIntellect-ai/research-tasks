You are a developer tasked with organizing a legacy project, migrating some logic to Python, and setting up a basic CI script to enforce security rules based on semantic versioning.

Your tasks are as follows:

1. **Organize the Project Structure:**
   Create the following directory structure:
   - `/home/user/project/`
   - `/home/user/project/proto/`
   - `/home/user/project/src/`
   - `/home/user/project/ci/`

   There are two protobuf files currently located in `/home/user/legacy_project/`. Move them into `/home/user/project/proto/`.

2. **Create a CI Build Script:**
   Write a Python script at `/home/user/project/ci/build.py`. This script must:
   - Scan the `/home/user/project/proto/` directory for `.proto` files.
   - Read the first line of each `.proto` file, which contains a comment like `// Version: X.Y.Z`.
   - Parse this version using semantic versioning rules.
   - For security reasons, any protobuf file with a version strictly less than `2.1.0` must be immediately deleted from the `proto/` directory.
   - For all remaining `.proto` files (version >= `2.1.0`), compile them into Python gRPC interfaces using `grpc_tools.protoc`. The generated `_pb2.py` and `_pb2_grpc.py` files must be placed in `/home/user/project/src/`.
   - After running successfully, the script should write a log file at `/home/user/ci_report.txt` containing the names of the `.proto` files that successfully passed the version check and were compiled, one per line.

3. **Translate Code and Implement the gRPC Server:**
   In `/home/user/legacy_project/`, there is a file named `auth_logic.rb` containing a token validation function written in Ruby.
   - Translate this Ruby logic into Python.
   - Write a gRPC server in `/home/user/project/src/server.py` that implements the `AuthService` defined in the secure protobuf file.
   - The server must expose the `VerifyToken` RPC. The RPC takes a `TokenRequest` (which has a `token` string) and returns a `TokenResponse` (which has a `valid` boolean). The `valid` field should be the result of your translated Ruby logic.
   - The server must listen on `[::]:50051`.

4. **Execution:**
   - Ensure the required dependencies (`grpcio`, `grpcio-tools`) are installed.
   - Run your `ci/build.py` script.
   - Start your `server.py` in the background and save its process ID to `/home/user/server.pid`.

Do not change the definitions within the `.proto` files, only process and use them.