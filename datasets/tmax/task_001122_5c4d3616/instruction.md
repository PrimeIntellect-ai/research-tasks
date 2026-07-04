You are a build engineer managing deployment artifacts. We are migrating a legacy C-based text validation library into a modern Go-based gRPC microservice.

Your task consists of four stages:

**1. Fix the Vendored C Library**
The source code for the legacy library is located at `/app/vendored/libtextverify`. 
- The `Makefile` is currently broken and fails to link the shared object (`libtextverify.so`) correctly. Fix the `Makefile` so that running `make` successfully compiles and links the shared library.
- The C code (`verify.c`) has a critical memory safety vulnerability (undefined behavior/buffer overflow) when processing large or specially encoded inputs. Identify and fix this vulnerability so it safely rejects invalid or overly large inputs instead of crashing. 

**2. Design the gRPC API**
Create a protobuf definition at `/home/user/grpc/verify.proto`.
- Define a service named `TextVerifier`.
- Define an RPC method `Verify` that takes a `VerifyRequest` (containing a `text` string field) and returns a `VerifyResponse` (containing a `valid` boolean field).
- Compile the protobuf file to Go code in the `/home/user/grpc/` directory.

**3. Implement the Go gRPC Server via CGO**
Write a Go gRPC server in `/home/user/server/main.go`.
- The server must implement the `TextVerifier` service.
- Use `cgo` to link against the newly built `/app/vendored/libtextverify/libtextverify.so`.
- The `Verify` method should pass the input text to the C function `int is_valid_text(const char* input);`. If the C function returns `1`, the text is valid. If it returns `0` (or if it violates length/safety constraints), it is invalid.
- The server should listen on `127.0.0.1:50051`.

**4. Build the Verification CLI**
Write a Go CLI program at `/home/user/scan_corpus/main.go` and compile it to an executable at `/home/user/scan_corpus/scanner`.
- The CLI must accept a directory path as a command-line argument (e.g., `./scanner /path/to/dir`).
- It must connect to the gRPC server at `127.0.0.1:50051`.
- It must read every file in the provided directory.
- For each file, it calls the gRPC `Verify` method with the file's contents.
- It must print exactly one line per file to standard output in this format:
  `<filename>: ACCEPTED` (if valid is true)
  `<filename>: REJECTED` (if valid is false)

Ensure your server runs in the background and the `scanner` executable is fully functional. We will test your `scanner` against our internal corpora.