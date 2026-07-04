You are tasked with fixing and testing a multi-language system involving a Rust WebSocket server and a Python test suite. 

The project is located at `/home/user/ws_server`. A new feature introducing JSON serialization/deserialization has been proposed, but the patch fails to compile due to Rust ownership and borrow checker errors. 

Your objectives are:
1. Apply the patch file `/home/user/feature.patch` to the `/home/user/ws_server` project.
2. Attempt to compile the project. You will notice borrow checker and ownership errors. Debug and fix the Rust code in `src/main.rs` so that it successfully compiles via `cargo build --release`. The fixed code must preserve the intended JSON parsing and WebSocket message handling logic.
3. Start the compiled server (`/home/user/ws_server/target/release/ws_server`) on port 8080 in the background.
4. Run the Python integration test `/home/user/test_client.py`. This script tests the WebSocket communication and serialization/deserialization endpoints. It will automatically generate a report at `/home/user/test_results.json` if successful.
5. We need to measure the memory usage of the server under load. Restart the server under the `time` command to capture memory profiling: `/usr/bin/time -v /home/user/ws_server/target/release/ws_server &> /home/user/memory_profile.txt &`. 
6. Run `/home/user/load_test.py`, which will send a burst of WebSocket messages to the server, then send a special `{"action": "shutdown"}` message to gracefully stop the server.
7. Wait for the server process to exit, completing the write to `/home/user/memory_profile.txt`.
8. Parse `/home/user/memory_profile.txt`, extract the numerical value for "Maximum resident set size (kbytes):", and write ONLY that integer to `/home/user/max_memory.txt`.

Ensure the server is thoroughly tested and the memory profile is properly captured. Do not change the Python scripts.