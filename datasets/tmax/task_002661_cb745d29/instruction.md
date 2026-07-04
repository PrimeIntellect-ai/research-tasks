You are an engineer setting up a polyglot build system and multi-service environment from scratch. We have a microservice architecture consisting of a Go-based API gateway, a Python backend, and a Redis cache. To ensure maximum performance and secure legacy integration, the payload sanitisation logic must be written in C++ and called from Go via Cgo.

Your task is to:
1. Implement the C++ sanitiser library.
2. Build a polyglot build system (Makefile) to compile the library and the Go gateway.
3. Configure and start the multi-service system so that an end-to-end flow can be tested.

### 1. C++ Sanitiser Library
Write your C++ implementation in `/home/user/project/src/sanitiser.cpp`.
It must expose the following C-compatible function:
`extern "C" bool is_safe_payload(const char* input);`

This function acts as a firewall classifier. It must parse the null-terminated `input` and return `false` (0) if the payload contains any of the following shell metacharacters: `|`, `;`, `&`, `$`, `>`, `<`, or `` ` `` (backtick). Otherwise, it must return `true` (1). 

### 2. Polyglot Build System
Create a `Makefile` at `/home/user/project/Makefile`. Running `make all` from `/home/user/project/` must:
- Compile `src/sanitiser.cpp` into a shared library at `build/libsanitiser.so`.
- Compile `src/gateway.go` into a Go executable at `build/gateway`. The Go compilation step must dynamically link against `libsanitiser.so`. Ensure `CGO_LDFLAGS` and `CGO_CFLAGS` or the compiler flags in your Makefile are set properly so the Go compiler can find your C++ headers/library.
*(Note: `gateway.go` is provided and already contains the Cgo import `// #include "sanitiser.h"`, but you must create `src/sanitiser.h` with the function declaration).*

### 3. Multi-Service Composition
The system relies on three services:
- **Redis**: Listens on TCP port 6379.
- **Python Backend**: A provided script at `/home/user/project/backend/app.py` runs a Flask server on port 5000. It expects a POST request at `/api` and writes the payload to Redis.
- **Go Gateway**: Listens on TCP port 8080. Exposes a POST endpoint at `/process`. It reads the payload, passes it to `is_safe_payload`, and if safe, forwards the request to the Python backend on port 5000. If unsafe, it returns HTTP 403.

Create a startup script at `/home/user/project/start.sh` that:
1. Starts the `redis-server` in the background.
2. Starts the Python backend in the background.
3. Configures the library path (e.g., `LD_LIBRARY_PATH`) and starts the built `build/gateway` in the background.
Wait a few seconds in the script to ensure all services are up. 

A verification script will test your end-to-end setup by sending HTTP POST requests to `http://127.0.0.1:8080/process` using payloads from two directories:
- Clean payloads (normal text) that must be accepted (HTTP 200).
- Evil payloads (containing shell injections) that must be rejected (HTTP 403).

Make sure all services are running and the end-to-end flow works before you finish.