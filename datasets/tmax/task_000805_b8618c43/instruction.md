As a QA engineer setting up our local test environment, I'm trying to run a hybrid Go-C gRPC microservice used for our new Web Security token validation pipeline. Unfortunately, the setup is broken.

I need you to fix the environment in `/home/user/token-env`. Here is the situation:

1. There is a legacy C library for token validation in `legacy_crypto.c`. The `Makefile` is broken—it's supposed to build a shared library `liblegacy_crypto.so` but fails because it's missing the necessary compiler flags for shared position-independent code.
2. The gRPC definition is in `service.proto`, but the Go stubs haven't been generated. 
3. The Go gRPC server (`server.go`) uses CGO to interface with the legacy C library. 
4. Whenever I start the server and run the test client (`go run client.go`), the server crashes due to a memory corruption issue in the C code when handling a 32-byte security token.

Your tasks:
1. Fix the `Makefile` to correctly build `liblegacy_crypto.so` (ensure it uses AddressSanitizer or standard flags so it compiles properly and can be linked by Go).
2. Generate the missing Go gRPC protobuf files from `service.proto`.
3. Debug the memory crash occurring in `legacy_crypto.c` (hint: look at how memory is allocated for the incoming token). Fix the C code.
4. Once the server runs without crashing, run `client.go`. It will output a successful validation message containing a 64-character hex signature.
5. Save exactly the output of the successful client run (just the text output from the client) into a file named `/home/user/token-env/qa_report.txt`.

Make sure `qa_report.txt` only contains the successful test response (e.g., "VALIDATION_SUCCESS: <signature>"). Do not include server logs in this file. Note: The `protoc` compiler and Go plugins (`protoc-gen-go`, `protoc-gen-go-grpc`) are already installed in the system. The Go module is initialized.