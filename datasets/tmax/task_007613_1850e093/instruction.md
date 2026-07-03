You are tasked with migrating a legacy Python 2 encryption component into a modern Go-based gRPC microservice. The old Python package has a broken `setup.py` that fails in Python 3, so we are completely replacing it with a Go service. Additionally, a downstream Rust formatting tool needs a quick fix.

Here is what you need to do:

1. **Analyze the Legacy Logic:** 
   Review the Python 2 script located at `/home/user/legacy/encrypt.py`. Understand the string manipulation logic it performs.

2. **Design the Protobuf Service:**
   Create a protobuf file at `/home/user/service/api.proto` with:
   - `syntax = "proto3";`
   - `package api;`
   - `option go_package = "./api";`
   - A service named `MigrationService`.
   - An RPC method `ProcessString` that takes a `StringRequest` (containing a single string field `payload = 1`) and returns a `StringResponse` (containing a single string field `result = 1`).

3. **Implement the Go gRPC Server:**
   Generate the Go protobuf files and implement the gRPC server in `/home/user/service/main.go`. 
   - The server must listen on TCP port `9090`.
   - The `ProcessString` implementation must exactly replicate the string manipulation logic from the legacy Python 2 script.
   - Start the Go server in the background.
   *(Assume `protoc` and the Go gRPC plugins are installed in the environment).*

4. **Fix the Rust Downstream Tool:**
   There is a Rust CLI tool at `/home/user/formatter/main.rs` that reads from standard input and formats the output. However, the author didn't understand Rust's ownership rules, and it currently fails to compile with a borrow checker error. 
   - Fix the compiler error in `/home/user/formatter/main.rs` without changing the intended logic (it should append ` [MIGRATED]` to the trimmed input).
   - Compile it using `rustc /home/user/formatter/main.rs -o /home/user/formatter/format_tool`.

5. **Verify the Integration:**
   A pre-written Go client is provided at `/home/user/client/main.go`. It connects to your server on port `9090`, sends the string `"legacy_python_code"`, and prints the response to stdout.
   - Run the client, pipe its output into your compiled Rust `format_tool`, and redirect the final output to `/home/user/final_result.txt`.