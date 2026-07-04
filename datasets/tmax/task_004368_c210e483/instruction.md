We have a legacy C++ data ingestion service that has recently been causing severe production issues. It is a long-running TCP server, but it suffers from a severe memory leak and periodically crashes when receiving malformed packets. 

You need to step in, debug the issues, and get a stable version of the server running.

Here is the situation:
1. **Source Code**: The source code is located in `/app/src/`. However, the previous engineer left it in an uncompilable state. You will need to fix the compiler and linker errors.
2. **Authentication**: The service requires a specific authentication token. The documentation for this token was lost, but we recovered a screenshot of the old design document at `/app/auth_spec.png`. You must extract the exact token from this image and ensure your fixed server checks for it.
3. **Corrupted Inputs**: We captured the network traffic right before the last crash. The capture is at `/app/traffic.pcap`. You must analyze this pcap to understand the structure of the normal and corrupted packets. The server must be fixed to gracefully reject the corrupted packets (returning an `ERROR\n` response) instead of crashing.
4. **Memory Leak**: Even when handling normal traffic, the service leaks memory. Identify the intermediate state or request handling step where memory is leaked, and fix it.

**Your objectives:**
- Fix the compiler and linker errors in `/app/src/server.cpp`.
- Read `/app/auth_spec.png` to find the secret authentication token. The server expects the client to send messages in the format: `AUTH <token>|DATA <payload>\n`.
- Analyze `/app/traffic.pcap` to identify the corrupted input causing the crash, and fix the C++ code to handle it without segfaulting or leaking memory.
- Fix the memory leak in the standard request processing loop.
- Compile the fixed server and run it. It must listen on TCP `127.0.0.1:9000`.
- The server must respond with `OK\n` for valid data with the correct token, `AUTH_FAIL\n` for incorrect tokens, and `ERROR\n` for gracefully handled corrupted data.

Leave the fixed server running in the background listening on `127.0.0.1:9000` so our test harness can verify it.