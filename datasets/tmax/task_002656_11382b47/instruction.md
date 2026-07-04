You are a developer organizing a project directory. A background service written in Go streams file organization patches over WebSockets, and a Rust client receives these patches to apply them to your project files. However, both the Go server and the Rust client are currently broken.

Your goal is to fix both components, verify the Rust logic using property-based testing, and successfully apply the patch.

Directory structure:
- `/home/user/ws_server/`: A Go WebSocket server.
- `/home/user/patch_client/`: A Rust client.
- `/home/user/project_files/`: Contains the target file `config.json`.

Tasks to complete:
1. **Fix the Go Server (`/home/user/ws_server/main.go`)**: The server reads a patch file and attempts to send it over a WebSocket connection using goroutines and channels, but it currently hangs due to a channel deadlock. Fix the concurrency issue so the server successfully binds to `127.0.0.1:8080` and transmits the text data when a client connects.
2. **Fix the Rust Client (`/home/user/patch_client/src/patcher.rs`)**: Implement the `apply_diff` function. It currently returns the original string. It must take an original string and a Unified Diff patch string, and return the patched string using the `diffy` crate. 
3. **Run the Property Test**: Verify your Rust implementation passes the existing property-based test in `patcher.rs` (`cargo test`).
4. **Execute the Pipeline**: 
   - Start the Go server in the background.
   - Run the Rust client (`cargo run`). The client is already programmed to connect to the Go server, receive the patch, read `/home/user/project_files/config.json`, apply the diff using your fixed `apply_diff` function, and save the result to `/home/user/project_files/config_fixed.json`.

Ensure `/home/user/project_files/config_fixed.json` is created with the correctly applied changes.