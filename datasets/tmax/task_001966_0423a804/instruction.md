You are a platform engineer responsible for maintaining the CI/CD pipeline's webhook ingestion system. We recently migrated to a highly optimized, custom C-based URL decoding library to sanitize incoming webhook payloads. However, the initial integration attempt failed, and the pipeline is currently offline.

We have vendored the source code for this C library at `/app/liburldecode`.

Your task requires you to fix the build system, patch a critical memory safety vulnerability in the C code, and create a Python-based REST API wrapper.

**Step 1: Fix the Build System**
The vendored library at `/app/liburldecode` contains a `Makefile`. It is supposed to compile both a shared library (`liburldecode.so`) and a command-line testing tool (`decode_cli`). Currently, the build fails. Fix the `Makefile` so that both targets compile successfully. Ensure the shared library is compiled with Position Independent Code (PIC).

**Step 2: Fix Memory Safety Bugs**
The C implementation in `urldecode.c` has a memory safety vulnerability (Undefined Behavior) when processing malformed percent-encoded sequences (e.g., `%2` at the end of a string, or `%2G`). 
Modify `urldecode.c` so that:
- Valid `%XX` hexadecimal sequences are correctly decoded.
- Malformed sequences (e.g., missing characters, non-hexadecimal characters) are left *exactly as they are* in the output without crashing or reading out of bounds.
The resulting binary `/app/liburldecode/decode_cli` takes a single argument (the string to decode) and prints the decoded string to `stdout`. Its output must perfectly match our secure reference implementation.

**Step 3: FFI & REST API integration**
Create a Python REST API using `FastAPI` at `/app/webhook_api.py`.
- It must load the repaired `/app/liburldecode/liburldecode.so` using Python's `ctypes` module.
- It must expose a `POST /decode` endpoint.
- The endpoint should accept a JSON body: `{"url": "<encoded_string>"}`.
- It must return a JSON response: `{"decoded_url": "<sanitized_string>"}`.
- Bind the server to `127.0.0.1:8000`.

To complete the task, ensure the C library is fully fixed, compiled, and the API script is written and functional.