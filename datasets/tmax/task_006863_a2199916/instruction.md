You are helping me fix and test a multi-file Rust WebSocket backend that handles structured data ingestion. 

Right now, the project in `/home/user/ws-ingest` fails to compile due to a few developer mistakes involving async operations, structured data parsing, and checksum calculation. 

Your objectives are:
1. **Fix the Rust Project**:
   - Investigate the compilation errors in `/home/user/ws-ingest`. The project consists of `main.rs`, `parser.rs`, and `checksum.rs`.
   - Fix the type mismatches in the JSON parser (`parser.rs`) and the CRC32 implementation (`checksum.rs`). Ensure the async WebSocket stream logic in `main.rs` compiles correctly.
   - Build the project using `cargo build` and start the server. By default, it runs on `127.0.0.1:9090`. Keep it running in the background.

2. **Configure Reverse Proxy**:
   - We need an Nginx reverse proxy in front of the backend. 
   - I have provided a base Nginx configuration at `/home/user/nginx_base.conf` which safely handles user-space permissions. 
   - Create a new configuration file at `/home/user/proxy.conf` that includes the contents of `nginx_base.conf` but adds an `http { server { ... } }` block.
   - The server should listen on `127.0.0.1:8080` and reverse proxy all requests to `127.0.0.1:9090`. Crucially, you must configure it to correctly proxy **WebSocket** connections (handle Upgrade headers).
   - Start Nginx in the background using: `nginx -c /home/user/proxy.conf`

3. **End-to-End Test**:
   - Write a Python test script at `/home/user/test_ws.py` to verify the whole stack.
   - The script should connect to the proxy at `ws://127.0.0.1:8080`.
   - It should construct a JSON payload with a `data` field set exactly to `"e2e_system_check"`.
   - It must compute the CRC32 checksum of the string `"e2e_system_check"`, and include it as an integer in the `checksum` field of the JSON payload.
   - Send the JSON payload over the WebSocket connection.
   - Await the response from the server, and write the raw text response to `/home/user/test_result.log`.

Requirements:
- Ensure the server and proxy are both running when you complete the task.
- The Rust application uses the `crc32fast` and `serde_json` crates.
- Python 3 is available; you may use the `websockets` library (`pip install websockets`) and the built-in `zlib` module for CRC32.