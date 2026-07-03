You are an integration developer tasked with testing a new high-performance WebSocket data ingestion pipeline. The architecture relies on a Python WebSocket client that receives binary data and offloads the parsing to a shared library written in Rust via an FFI (Foreign Function Interface) C-ABI. 

Currently, the system is broken:
1. The Rust parser library has a memory/borrow checker bug preventing it from safely compiling and executing.
2. The Python integration benchmark client needs to be written from scratch.

Your task is to fix the Rust library, compile it, and write a Python benchmark client to test the pipeline.

**Phase 1: Fix and Compile the Rust Shared Library**
A Rust project is located at `/home/user/parser`. It exposes an FFI function `decode_message` that takes a custom byte-packed encoded buffer (1st byte is encoding type: `0` for UTF-8, `1` for UTF-16LE; the rest is the payload) and returns a valid UTF-8 C-string. 
However, the original developer made a borrow checker / lifetime mistake when returning the C-string pointer.
- Fix the bug in `/home/user/parser/src/lib.rs` so it safely hands over ownership of the string to C. (You do not need to implement a memory freeing function for this specific benchmark).
- Compile the library in release mode so that `/home/user/parser/target/release/libparser.so` is produced.

**Phase 2: Start the Test Server**
A local WebSocket server is provided at `/home/user/server.py`. 
- Start it in the background. It will listen on `ws://127.0.0.1:8765`. Once a client connects, it will rapidly stream exactly 100 binary messages and then close the connection.

**Phase 3: Write the Python Benchmark Client**
Write a Python script at `/home/user/client.py` that:
1. Loads `/home/user/parser/target/release/libparser.so` using `ctypes`.
   - The C signature you must bind to is: `char* decode_message(const uint8_t* data, size_t len);`
2. Connects to `ws://127.0.0.1:8765` using the `websockets` library.
3. Records the start time (using `time.perf_counter()`).
4. Receives all 100 binary messages from the server.
5. For each message, passes the binary payload to the Rust `decode_message` function via `ctypes` and decodes the returned pointer into a Python string.
6. Records the end time.
7. Creates a file `/home/user/benchmark_result.json` with the following exact JSON structure:
```json
{
  "message_count": 100,
  "total_time_ms": 15.42,
  "last_message_decoded": "VALIDATION_STRING_XYZ"
}
```
*Note: `total_time_ms` must be a float representing the total time taken to receive and process all messages in milliseconds. `last_message_decoded` must be the exact string value of the 100th (final) message.*

**Environment:**
- A Python virtual environment is available at `/home/user/venv`. The `websockets` package is already installed. Ensure you use `/home/user/venv/bin/python` to run your scripts.
- Cargo and rustc are installed and available in the PATH.