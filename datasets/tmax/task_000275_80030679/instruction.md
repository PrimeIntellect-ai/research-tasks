You are helping a developer migrate a large number of legacy Python 2 packages to Python 3. Because of the volume, the team has decided to build a high-performance, centralized Go-based patching service using gRPC.

Your task is to implement this gRPC patching service, compile the protobuf, and use it to patch a broken Python 2 `setup.py`.

Work inside `/home/user/workspace/`.

1. **Protobuf Definition**: Create a file `/home/user/workspace/migration.proto` with the following specifications:
   - Uses `proto3`.
   - Package name: `migration`.
   - Go package option: `./migration`.
   - Define an enum `Op` with three values: `KEEP = 0`, `ADD = 1`, `DELETE = 2`.
   - Define a message `Change` with fields: `Op op = 1` and `string line = 2`.
   - Define a message `PatchRequest` containing a list of `Change` messages (field `repeated Change changes = 1;`).
   - Define a message `PatchResponse` containing `string patched_code = 1;`.
   - Define a service `Patcher` with an RPC `Apply` that takes a `PatchRequest` and returns a `PatchResponse`.

2. **Code Generation**: Use `protoc` to generate the Go code in `/home/user/workspace/migration/`. (Assume `protoc` and Go plugins are installed).

3. **Data Structure & Server Implementation**: Create `/home/user/workspace/server.go`.
   - Implement a custom data structure `type TextBuffer struct { lines []string }` with methods `Append(line string)` and `Render() string` (which joins the lines with a newline `\n`).
   - Implement the gRPC `PatcherServer` interface. The `Apply` method should iterate through the changes in the `PatchRequest`.
     - If the operation is `KEEP` or `ADD`, append the line to the `TextBuffer`.
     - If the operation is `DELETE`, do nothing (discard the line).
   - The server must listen on `localhost:50051`.

4. **Execution**:
   - I have provided a client script at `/home/user/workspace/client.go` that connects to `localhost:50051`, sends a hardcoded Python 2 to Python 3 migration patch sequence for a `setup.py` file, and writes the resulting text to `/home/user/workspace/patched.py`.
   - Run your server in the background, then execute `go run client.go`.

Ensure the final output file `/home/user/workspace/patched.py` is correctly generated.