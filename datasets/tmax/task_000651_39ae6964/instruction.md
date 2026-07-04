You are acting as a Release Manager preparing the backend systems for an upcoming critical software deployment. As part of our deployment pipeline, we need a robust validation service that can receive binary patches, apply them to base files, and verify the structural integrity of the patched files using our proprietary error-correcting signature algorithm.

You have been provided with an incomplete and broken workspace in `/home/user/workspace/`. 
Your objective is to fix the components, build them, and launch the validation service.

Here are the specific requirements:

1. **The Validation Oracle (`/app/sig_gen`)**
   We have a proprietary signature generator compiled as a stripped binary located at `/app/sig_gen`. 
   If you run `/app/sig_gen <file_path>`, it outputs a hexadecimal mathematical checksum of the file's contents to `stdout`.

2. **The C++ Validation Server (`/home/user/workspace/cpp_server/`)**
   This directory contains the source code for a TCP server written in C++. It is supposed to listen for incoming validation requests, but the `Makefile` is broken, and there are compilation errors in `server.cpp` (missing includes and incorrect standard library usage).
   - Fix the `Makefile` and `server.cpp` so it compiles cleanly using `make`.
   - The server must bind to `127.0.0.1:8080`.
   - **Protocol Specifications:**
     The server speaks a simple newline-terminated TCP protocol.
     A client sends a single line: `VALIDATE <base64_base_file> <base64_patch_file>`
     The server must:
       a) Decode the base64 contents and save them to temporary files.
       b) Apply the patch to the base file using the standard Unix `patch` utility.
       c) Run `/app/sig_gen` on the successfully patched file.
       d) Return a single line to the TCP client: `SUCCESS <signature>` (where signature is the exact output of `sig_gen`).
       e) If patching fails, return `ERROR PATCH_FAILED`.
   - Once compiled, start the C++ server in the background so it is actively listening on port 8080.

3. **The Go Deployment Runner (`/home/user/workspace/go_runner/`)**
   This directory contains a Go tool (`main.go`) used to concurrently blast the C++ server with deployment fragments to ensure it can handle parallel patch verifications.
   - The Go code has a concurrency bug. It uses goroutines and channels, but it often panics or exits before all jobs are completed due to a data race and improper `sync.WaitGroup` usage.
   - Fix the Go code so that `go run main.go` executes successfully, connects to the C++ server on port 8080, processes all 50 concurrent validation checks without hanging, and exits cleanly with code 0.

Ensure the C++ server remains running on `127.0.0.1:8080` when you are finished, as our automated test suite will connect to this port and send protocol-level validation requests to ensure your system works perfectly.