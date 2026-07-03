You are a developer working on a custom Build Orchestration system written in Go. This system acts as a remote test orchestrator and build command emulator, communicating via WebSockets. It is used to build and test a multi-file Rust project.

Currently, the setup is broken in three ways:
1. The Go WebSocket server (`/home/user/go_orchestrator/server.go`) has a bug in its command interpreter. It is supposed to parse incoming text commands (like `BUILD <path>` and `RUN <path>`), execute the corresponding `cargo` commands using `os/exec`, and send back the results. However, it currently fails to parse arguments correctly.
2. The target Rust project (`/home/user/rust_target`) has a deliberate compilation error in its source code.
3. The end-to-end test script is missing.

Your tasks are as follows:

1. **Fix the Rust Project:**
   Navigate to `/home/user/rust_target`. Inspect the source code (specifically `src/main.rs` and `src/helper.rs`) and fix the compilation error so that `cargo build` and `cargo run` succeed. The program, when run, should print `Hello from the helper!`.

2. **Fix the Go Server:**
   Navigate to `/home/user/go_orchestrator`. Look at `server.go`. It uses the `github.com/gorilla/websocket` library. There is a bug in the interpreter loop where it parses incoming messages. It currently splits the command string incorrectly, causing the executor to fail. Fix the parsing logic so it correctly splits commands by spaces. 
   *(Note: You may need to run `go mod tidy` or install dependencies).*

3. **Create the E2E Test Script:**
   Create a file named `/home/user/test_script.txt`. It must contain exactly two lines in this custom interpreted language:
   ```
   BUILD /home/user/rust_target
   RUN /home/user/rust_target
   ```

4. **Run the E2E Orchestration:**
   - Start the Go server in the background (`go run server.go &`). It will listen on `ws://localhost:8080/ws`.
   - Use the provided Go client (`/home/user/go_orchestrator/client.go`) to execute the test script:
     `go run client.go -script /home/user/test_script.txt -output /home/user/e2e_report.json`

The client will read the script, send the commands sequentially via WebSocket to the server, and write the server's JSON responses to `/home/user/e2e_report.json`. 

Verify that `/home/user/e2e_report.json` is generated and contains the successful build and run output of the Rust project.