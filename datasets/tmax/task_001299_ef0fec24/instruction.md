You are tasked with fixing and securing a polyglot build system orchestrator. The project is located in `/home/user/app`. 

Currently, the system is designed to accept polyglot build jobs via a gRPC interface, queue them, and stream build execution logs back to clients via WebSockets. However, the system is broken and lacks security validation for incoming build payloads.

Your objectives are:

1. **Service Configuration & Integration:**
   The multi-service stack consists of three components defined in `/home/user/app/docker-compose.yml` (or run natively via a startup script `/home/user/app/start_services.sh`):
   - A Redis queue backend.
   - A Go-based gRPC Job Dispatcher.
   - A Node.js WebSocket log streamer.
   Currently, the gRPC dispatcher and the WebSocket streamer cannot communicate due to mismatched configuration and missing protobuf implementations. 
   - Compile the missing protobuf definitions in `/home/user/app/proto/build.proto` for Go.
   - Reconfigure the environment variables in `/home/user/app/.env` so the Go gRPC service correctly connects to Redis on port 6379 and the WebSocket streamer on port 8080.

2. **Adversarial Build Payload Validator:**
   We have a major security issue: malicious users are submitting build jobs with commands that attempt to break out of the build emulator. 
   - Write a Go-based CLI tool at `/home/user/app/validator/main.go`.
   - This tool must accept a single command-line argument containing the path to a JSON build definition file.
   - It must analyze the "steps" array in the JSON. It must safely preserve and accept valid build configurations (exit code 0) and reject payloads containing malicious shell escapes, unauthorized network calls, or memory exhaustion attempts (exit code 1).
   - Your validator will be tested against two corpora: `/home/user/app/corpus/clean/` (which contains valid polyglot build definitions) and `/home/user/app/corpus/evil/` (which contains payloads designed to exploit the build worker). 
   - To pass, your validator must achieve 100% accuracy: rejecting all evil payloads and accepting all clean payloads.

3. **Log Streamer Translation & Fix:**
   The WebSocket log streamer prototype was originally written in Python (`/home/user/app/python_logger/logger.py`) but causes memory leaks. Translate its core message-parsing logic into Go and integrate it directly into the Go dispatcher so that as the emulator executes the build, memory-profiled WebSocket updates are pushed to port 8081.

Verify your setup by running the local integration test script: `/home/user/app/verify_e2e.sh`. Leave the system running and the validator compiled at `/home/user/app/bin/validator`. Do not hardcode the test payloads; implement a robust detection algorithm using regex or AST parsing.