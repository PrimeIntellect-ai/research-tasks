I need you to help me organize and modernize a legacy project archive. We have a set of project files and an old C library that calculates specific checksums, and I want to expose this functionality over a modern WebSocket interface for our internal tools. 

Here are the requirements:

1. **Extract Authentication Token**: There is an image file located at `/app/project_auth.png`. This image contains a handwritten authentication token (a 12-character alphanumeric string). You need to extract this token (using OCR, e.g., `pytesseract`).
2. **Compile and Wrap the C Library**: In `/home/user/legacy_lib/`, there is a C file `custom_hash.c`. Compile it into a shared library (`libcustom_hash.so`). Then, write a Python wrapper using `ctypes` that can call the `compute_hash` function from this library.
3. **Build a WebSocket Server**: Create a Python WebSocket server that listens on `127.0.0.1:8765`. 
4. **Implement the Protocol**:
   - The server must require clients to send an authentication message first: `{"type": "auth", "token": "<EXTRACTED_TOKEN>"}`. If the token is incorrect, close the connection.
   - Once authenticated, the server should accept a message of type `organize`: `{"type": "organize", "files": ["file3.txt", "file1.txt", "file2.txt"]}`.
   - The server must sort the file names alphabetically, and for each file name, compute its custom hash using the C library.
   - The server should respond with: `{"type": "result", "sorted_files": [...], "hashes": [...]}`.
5. **Write Tests**: Write a `pytest` suite in `/home/user/tests/test_server.py` that starts the server, connects to it via websockets, authenticates, and verifies the sorting and hashing functionality. Ensure the tests pass.

Leave the WebSocket server running as a background process (or daemon) listening on `127.0.0.1:8765` so my automated verification script can connect to it. Save your server script at `/home/user/server.py`.