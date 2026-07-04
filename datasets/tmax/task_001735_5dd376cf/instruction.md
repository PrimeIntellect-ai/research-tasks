You are tasked with porting a critical inline WebSocket firewall to a minimal container environment (which lacks standard shared libraries like glibc). To achieve this, you need to write a static C++ WebSocket server, fix a broken vendored dependency, and ensure it correctly filters malicious payloads.

**Phase 1: Fix the Vendored Dependency**
We use the lightweight `mongoose` networking library for our WebSocket server. The source for version 7.11 is pre-vendored at `/app/vendored/mongoose`.
However, the previous maintainer hardcoded the `Makefile` in that directory to always build a dynamic shared object (`libmongoose.so`), completely ignoring environment variables and preventing static linking. 
1. Fix the `/app/vendored/mongoose/Makefile` so that it builds a static library (`libmongoose.a`) when `make static` is invoked.

**Phase 2: Write the WebSocket Firewall in C++**
Write a C++ program at `/home/user/ws_firewall.cpp` that embeds the `mongoose` server.
- The server must listen for WebSocket connections on port `8080`.
- When a WebSocket message is received, it must inspect the payload (which will be plain text).
- **Filter Rules:** If the payload contains the exact substring `<script>` (XSS attempt) OR the exact substring `DROP TABLE` (SQLi attempt), the server must reply via the WebSocket with the exact string `REJECT`.
- If neither substring is present, it must reply with the exact string `ACK`.
- The server should keep running and processing messages.

**Phase 3: Cross-Compilation / Static Build**
Compile your C++ program statically to ensure it runs in our minimal scratch container.
- Use the fixed static `libmongoose.a`.
- The final binary must be located at `/home/user/ws_firewall_bin`.
- Ensure `file /home/user/ws_firewall_bin` shows it is "statically linked".

**Phase 4: Performance Benchmarking**
Start your server in the background. We have provided a benchmarking script at `/app/bench_tool.sh` that connects to `ws://localhost:8080` and blasts it with 500 WebSocket messages.
Run this script: `/app/bench_tool.sh`
Redirect its standard output to `/home/user/bench_results.txt`.

Ensure your server remains running on port 8080 when you finish the task, as the automated test suite will connect to it to run the adversarial corpus tests.