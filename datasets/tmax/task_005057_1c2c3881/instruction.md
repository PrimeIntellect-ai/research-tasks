You are tasked with setting up a secure polyglot build system and API gateway from scratch. We have a microservice-based web system with components written in Rust, Go, C, and Python. However, the existing code has several critical security and compilation issues. 

Your objective is to fix the compilation/security bugs in the lower-level components, and then write a secure Python orchestration script that builds them and serves as a Web Gateway.

Here is the current state of the workspace (which you will find in `/home/user/polyglot/`):
1. `validator.rs`: A Rust module intended to validate token signatures. It currently fails to compile due to a lifetime issue (a borrowed reference outlives its owner).
2. `parser.c`: A C program that compiles to a shared library (`libparser.so`). It parses incoming payload strings but currently contains a buffer overflow vulnerability (uses `strcpy` instead of bounds-checked functions).
3. `logger.go`: A Go application that logs access records concurrently. It currently has a race condition because multiple goroutines write to a shared map without a mutex.

**Your specific tasks:**

1. **Fix the code:** 
   - Modify `/home/user/polyglot/validator.rs` so that it compiles successfully (fix the ownership/lifetime error) without changing its public signature.
   - Modify `/home/user/polyglot/parser.c` to use `strncpy` instead of `strcpy` to prevent buffer overflows, ensuring the buffer size is capped at 256 bytes.
   - Modify `/home/user/polyglot/logger.go` to use a `sync.Mutex` when writing to the shared global map `LogMap`.

2. **Write the Build & Gateway Script (`/home/user/gateway.py`):**
   Write a Python script from scratch at `/home/user/gateway.py`. This script must:
   - Compile the Rust code: `rustc validator.rs -o validator`
   - Compile the C code: `gcc -shared -o libparser.so -fPIC parser.c`
   - Compile the Go code: `go build -o logger logger.go`
   - (The script should use Python's `subprocess` module to run these build commands and verify they return exit code 0).
   - Once built, the script should expose a simple HTTP server on port `8080`.
   - The server must have an endpoint `POST /process` that accepts a JSON payload: `{"token": "...", "data": "..."}`.
   - The Python script must securely deserialize the JSON payload, pass the `"token"` to the Rust `validator` binary via standard input, and check if it returns "VALID".
   - If valid, write a success message to `/home/user/build_output.log` containing the text: "BUILD_AND_SECURE_COMPLETE".

**Verification Requirements:**
- The agent must successfully fix all three polyglot files.
- The Python script `/home/user/gateway.py` must be executable and successfully build the three binaries.
- Once `/home/user/gateway.py` is run and tested, it must create `/home/user/build_output.log` with the exact success string.