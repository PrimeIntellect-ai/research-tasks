You are an engineer tasked with setting up a polyglot build system and network service from scratch for a new Web Security tool. We have a highly optimized payload sanitizer written in C, but we need to expose it via a WebSocket server written in a modern language of your choice.

Your task is to implement the build system, package management, and the WebSocket server implementation. 

We have provided the C source code for the sanitizer at `/home/user/project/src/sanitizer.c`. It contains a single function:
`int is_safe_payload(const char* payload);`
This function returns `1` if the payload is safe, and `0` if it contains malicious signatures.

Please complete the following objectives:

1. **Build System**: Create a `Makefile` at `/home/user/project/Makefile`. When `make` is executed in that directory, it should compile `/home/user/project/src/sanitizer.c` into a shared dynamic library named `libsanitizer.so` and place it in `/home/user/project/build/`.
2. **Package Management & WebSocket Server**: 
   - Choose a language (e.g., Python, Node.js, Ruby, etc.) and set up its package management within `/home/user/project/server/` (e.g., `requirements.txt`, `package.json`, etc.). 
   - Write a WebSocket server in that directory. The server must listen on `ws://127.0.0.1:8765`.
   - The server must dynamically link/load the compiled `libsanitizer.so` library.
   - For every incoming WebSocket text message, pass it to `is_safe_payload`.
   - If the payload is safe (returns `1`), the server must send back the exact string: `SAFE: <original_message>`.
   - If the payload is malicious (returns `0`), the server must send back the exact string: `REJECTED`.
3. **Execution Script**: Create a bash script at `/home/user/project/start.sh` that:
   - Sets up/installs any dependencies needed by your server.
   - Runs `make` to build the C library.
   - Starts the WebSocket server in the background.
   - Writes the PID of the background WebSocket server process to `/home/user/project/server.pid`.
   - Ensure the script is executable (`chmod +x`).

Notes:
- You are free to choose the language for the WebSocket server, as long as it operates over standard WebSockets.
- Ensure your server stays running to accept multiple consecutive messages.