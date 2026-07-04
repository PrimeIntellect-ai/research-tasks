You are tasked with helping our infrastructure team migrate a critical legacy system from Python 2 to Python 3. The system relies heavily on a polyglot architecture where Python services communicate with a high-performance C++ shared library via C-FFI (ctypes). 

Due to the transition, we are experiencing ABI management issues—specifically, Python 3 handles strings as Unicode by default, whereas Python 2 used bytes. Passing a Python 3 string directly to a C function expecting `char*` causes memory corruption and silent truncation.

Your task consists of two parts:

### Part 1: ABI Compatibility Linter (Adversarial Corpus)
You must write a strict Bash script, `/home/user/app/abi_linter.sh`, that statically analyzes Python source files to ensure they are safe for Python 3 FFI.
The script must take a single file path as its argument.
- It should print exactly `ACCEPT` to stdout and exit with 0 if the file is safe.
- It should print exactly `REJECT` to stdout and exit with 1 if the file contains unsafe C-FFI patterns.

A file is considered "unsafe" (evil) if it contains a ctypes function call where a plain string literal (e.g., `"my_string"` or `'my_string'`) is passed to a C function, WITHOUT an explicit `b` prefix (e.g., `b"my_string"`) or a `.encode()` call on the same line. 
A file is "safe" (clean) if all string literals passed to C functions are explicitly byte-prefixed or encoded, OR if the file does not use ctypes at all.
You can assume ctypes C function calls in our codebase always look like `lib.some_function(...)`.

To help you develop this, we have provided two corpora of Python files:
- `/home/user/app/corpus/clean/`: Contains 10 Python 3 safe FFI bindings.
- `/home/user/app/corpus/evil/`: Contains 10 Python 2 legacy bindings that will cause segfaults in Python 3.
Your linter must achieve 100% accuracy on this corpus.

### Part 2: Polyglot Service Orchestration
We are running a multi-service environment simulating our production rollout. In `/home/user/app/compose`, there are three services managed by a custom startup script `start_services.sh`:
1. `legacy_py2_worker` (listens on `127.0.0.1:9002`)
2. `modern_py3_worker` (listens on `127.0.0.1:9003`)
3. `c_ffi_backend` (a C++ emulator gRPC service on `127.0.0.1:50051` used by both workers)

You must write a Bash-based traffic router `/home/user/app/router.sh` that listens on `127.0.0.1:8080` (using `socat`, `nc`, or standard Bash utilities). 
This router must accept incoming JSON HTTP POST requests. 
- If the JSON payload contains `"version": 2`, the router must forward the payload to the legacy worker (`9002`) and return its response.
- If the JSON payload contains `"version": 3`, it must forward the payload to the modern worker (`9003`) and return its response.

Make sure your router handles incoming TCP connections cleanly and closes them after returning the response. You must leave the router running in the background or provide instructions on how to start it so our automated verification suite can test the end-to-end flow.

Create a log file `/home/user/app/router_access.log` where your router logs every request it receives in the format: `[TIMESTAMP] ROUTED TO <version>`.

Complete both components. Ensure your linter script has executable permissions.