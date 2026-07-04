You are tasked with fixing a broken build artifact processing pipeline. As a build engineer, you manage artifacts by hashing them and tracking changes between builds.

Currently, we have a high-performance hashing library written in Rust located at `/home/user/rust_hasher`. It is designed to expose a C-FFI for Python to consume. However, it currently fails to compile due to lifetime/borrowing issues in its FFI boundary (`src/lib.rs`). 

Your tasks are as follows:

1. **Fix the Rust Library**:
   Navigate to `/home/user/rust_hasher`. The function `calculate_artifact_checksum` is intended to compute an Adler-32-like checksum of a byte buffer and return a hex string via C-FFI. However, it improperly handles CString memory lifetimes, causing compiler errors or dangling pointers. Fix the lifetime issue so it safely returns a dynamically allocated `*mut c_char`. Make sure it compiles into a shared library (`target/release/librust_hasher.so`) using `cargo build --release`.

2. **Write the Python Artifact Server**:
   Create a Python script at `/home/user/artifact_server.py`. 
   This script must:
   - Use `ctypes` to load `librust_hasher.so` and wrap the `calculate_artifact_checksum` function (and the `free_checksum` function, to avoid memory leaks).
   - Start a WebSocket server on `ws://localhost:8765` using the `websockets` and `asyncio` libraries.
   - Maintain a state of the "previous build's" artifact hashes. (Initially empty).

3. **WebSocket Protocol**:
   When the server receives a JSON message, it will be in this format:
   `{"id": "build-123", "files": ["/home/user/artifacts/bin1", "/home/user/artifacts/bin2"]}`

   For each request, the server must:
   - Read the raw bytes of each file in the `files` list.
   - Call the Rust FFI function to get the checksum string for those bytes.
   - Sort the files alphabetically by their **file path**.
   - Compare the new hashes against the hashes from the *immediately preceding* request to compute a diff.
   - Send back a JSON response strictly matching this structure:
     ```json
     {
       "id": "build-123",
       "sorted_hashes": [
         {"file": "/home/user/artifacts/bin1", "hash": "00000abc"},
         {"file": "/home/user/artifacts/bin2", "hash": "00000def"}
       ],
       "diff": {
         "added": ["/home/user/artifacts/bin1", "/home/user/artifacts/bin2"],
         "removed": [],
         "modified": []
       }
     }
     ```
     *(Note: "added" means the file path wasn't in the previous request. "removed" means a file path from the previous request is missing in the current one. "modified" means the file path is present in both, but the hash changed. Arrays in the diff should be sorted alphabetically by file path).*

   Update the server's state so the current request's hashes become the "previous" ones for the next request.

Keep the server running in the background or ready to be executed via `python3 /home/user/artifact_server.py`. Once the server is written and running, write a file `/home/user/done.txt` containing the word `READY`.