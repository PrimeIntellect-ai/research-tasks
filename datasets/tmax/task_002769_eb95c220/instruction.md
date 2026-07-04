You are tasked with organizing a messy directory of security tools, patching a vulnerable C++ REST API, and verifying its functionality by crafting a specific assembly payload.

Currently, in `/home/user/legacy_tools`, there are several files dumped together:
- `api_server.cpp`: A C++ source file for a simple web server (using standard sockets, no external dependencies).
- `b64_decoder.patch`: A unified diff file meant to fix a bug in the server's base64 decoding function.
- `payload_validator.h`: A header file used by the server to ensure incoming assembly payloads do not contain forbidden instructions.

Perform the following tasks:

1. **Organize the Project:**
   Create a new directory structure at `/home/user/sec_api/` with the following subdirectories:
   - `src/` (move `api_server.cpp` here)
   - `include/` (move `payload_validator.h` here)
   - `patches/` (move `b64_decoder.patch` here)
   - `build/` (for the compiled binary)

2. **Patch and Compile:**
   - Apply `b64_decoder.patch` to `api_server.cpp`.
   - Compile the patched `api_server.cpp` into an executable named `server` inside `/home/user/sec_api/build/`.
   - Ensure you include the `include/` directory in your compilation paths (e.g., `-I../include`). Compile with `-std=c++17`.

3. **Run the Server:**
   - Start the compiled `server` in the background. It will automatically listen on `127.0.0.1:8080`.

4. **Craft the Payload and Verify:**
   - The server exposes a POST endpoint at `http://127.0.0.1:8080/analyze`.
   - It expects a plain-text HTTP body containing a **Base64-encoded** x86-64 machine code payload.
   - Craft an x86-64 assembly payload that does exactly the following: Sets the `RAX` register to the decimal value `42` (using a 32-bit immediate `mov` to `eax` or `rax`), and then returns (`ret`). The payload must be minimal. 
   - Base64-encode these exact raw machine code bytes.
   - Use `curl` to send a POST request with this Base64 string as the body to the `/analyze` endpoint.
   - Save the exact HTTP response body returned by the server into `/home/user/sec_api/response.log`.