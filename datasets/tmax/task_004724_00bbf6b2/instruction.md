You are an engineer setting up a new polyglot build system from scratch. Your task is to implement the "Build Broker", a Rust-based API that routes build requests, parses a custom build-script mini-language, applies rate limiting, and dispatches the build commands to a worker node via WebSocket.

Create a new Rust project named `build_broker` in `/home/user/build_broker`.
You must write the application to meet the following specifications:

1. **URL Routing & Server:**
   - The Rust server must listen on `127.0.0.1:8080`.
   - Implement an HTTP POST endpoint at `/api/build/:target` (where `:target` is a dynamic URL parameter).

2. **Request Validation & Rate Limiting:**
   - **Validation:** The `:target` must be exactly `rust` or `cpp`. If any other target is requested, return an HTTP 400 Bad Request status code.
   - **Rate Limiting:** A specific `:target` can only receive one build request per second. If a request for a target is received less than 1 second after a previous successful request for the *same* target, return an HTTP 429 Too Many Requests status code.

3. **Mini-Language Interpreter:**
   The HTTP POST request body will contain a plain text custom build script. You must parse this script line by line.
   - `CMD <string>`: Sets the build command.
   - `ENV <key>=<value>`: Adds an environment variable.
   - `RUN`: Indicates the script is ready to be dispatched.
   - Ignore empty lines.
   - If `RUN` is encountered, immediately stop parsing and dispatch the job. If the script ends without `RUN`, do nothing and return HTTP 200.

4. **WebSocket Dispatch:**
   - When a `RUN` command is interpreted, the server must format the job as a JSON object: 
     `{"target": "<target_from_url>", "cmd": "<cmd_string>", "env": {"<key>": "<value>"}}`
   - Connect to the worker WebSocket server at `ws://127.0.0.1:9000/dispatch` and send the JSON string as a single text message. (Do not keep the connection open indefinitely; you can connect, send, and close per `RUN`, or maintain a pool, but sending the text message is the requirement).
   - Return an HTTP 200 OK after dispatching.

**Testing Environment:**
A Python WebSocket server is already running locally on port 9000. It logs received JSON payloads. Do not modify or interact with port 9000 directly via curl; your Rust server must act as the WebSocket client.

**Requirements:**
- Use Rust. You may use standard libraries and community crates (e.g., `axum`, `tokio`, `tokio-tungstenite`, `serde_json`, `futures-util`). 
- Start the server as a background process or leave it running in a `tmux` session when you are finished so it can be verified. Write the output to `/home/user/broker.log`.