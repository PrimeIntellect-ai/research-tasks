You are a mobile build engineer maintaining a custom build orchestration pipeline. A recent migration left several micro-tools in a broken state, and the main orchestrator needs to be rewritten. 

Your task is to fix the broken tools and implement a new orchestrator service.

### 1. Fix the Rust Expression Evaluator
There is a Rust project at `/home/user/rust_eval`. It is meant to parse build constraints, but it currently fails to compile due to ownership and borrow checker errors.
- Fix the compiler errors in `/home/user/rust_eval/src/main.rs`.
- Ensure it successfully builds via `cargo build`.
- When run as `./target/debug/evaluator "<expr>"`, it should output the parsed AST in JSON format on the last line of standard output.

### 2. Fix the C++ Cache Tool
There is a C++ utility at `/home/user/cpp_cache`. It computes cache keys for build artifacts. It currently compiles but frequently segfaults due to memory safety issues (undefined behavior and out-of-bounds access).
- Fix the memory safety issues in `/home/user/cpp_cache/main.cpp`.
- Compile it using `g++ -o cacher main.cpp`.
- It must not segfault or leak memory when processing large strings.
- When run as `./cacher "<data>"`, it should print the computed cache hash to standard output.

### 3. Integrate the Legacy Mobile Signer
We have a proprietary, stripped binary located at `/app/mobile_signer`. We do not have the source code for this.
- It takes a single command-line argument: the absolute path to a file.
- It reads the file and outputs a hex-encoded signature to standard output.
- You will need to treat this as a black box and integrate it into your orchestrator.

### 4. Build the Orchestrator API
Create a new HTTP service (in any language of your choice: Python, Node.js, Go, etc.) that binds to `127.0.0.1:8080`.
It must expose a single endpoint:
- **POST `/process`**
- **Payload:** JSON in the format `{"expr": "<string>", "cache_data": "<string>", "file_path": "<string>"}`
- **Action:**
  1. Execute the fixed Rust evaluator with the provided `expr`. Parse its final line of output as JSON.
  2. Execute the fixed C++ cacher with the provided `cache_data`. Capture its output as a string (trimmed of whitespace).
  3. Execute the `/app/mobile_signer` binary passing the `file_path`. Capture its output as a string (trimmed of whitespace).
- **Response:** JSON in the format:
  ```json
  {
    "ast": <json_object_from_rust_tool>,
    "hash": "<string_from_cpp_tool>",
    "signature": "<string_from_mobile_signer>"
  }
  ```

Start your HTTP service in the background or leave it running in the terminal. Once the service is listening on port 8080, write a file to `/home/user/ready.txt` containing the word `READY`. Our automated verification system will then send test requests to your API.