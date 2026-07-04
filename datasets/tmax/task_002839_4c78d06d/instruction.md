I am trying to organize my polyglot build system. We have a legacy, stripped compilation analysis tool located at `/app/build_analyzer`. I need you to write a Rust service that exposes this tool over WebSockets so my other build orchestration scripts can query it dynamically.

Here is what you need to do:
1. Create a new Rust project in `/home/user/build_proxy`. 
2. Write a Rust WebSocket server that listens on `127.0.0.1:9050` at the `/analyze` endpoint.
3. The server must accept WebSocket text messages. The incoming messages will be JSON in the format: `{"target_file": "/path/to/some/file.txt"}`.
4. For each incoming message, your server must extract the `target_file` path, and execute the binary `/app/build_analyzer` with the file path as its only command-line argument.
5. Capture the standard output of the `/app/build_analyzer` tool and send it back over the same WebSocket connection as a plain text string. If the JSON is malformed or the file doesn't exist, send back the string `ERROR`.
6. Compile the Rust project in release mode and leave the server running in the background (e.g., `cargo run --release &`) so it can be queried by our network tests.

Please ensure the server handles multiple consecutive messages on the same connection.