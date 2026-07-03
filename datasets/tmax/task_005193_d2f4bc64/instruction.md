You are an AI assistant helping a QA engineer set up a test environment for a new polyglot microservice architecture. The environment consists of a Go-based gRPC service that uses a C library via `cgo`, a Redis instance for rate limiting, and a Python HTTP gateway. 

Currently, the setup is broken. The project is located in `/home/user/app`.

Here is what you need to do:

1. **Fix the C Library Build and Linkage**:
   There is a C library in `/home/user/app/c_src`. It uses CMake. The Go service in `/home/user/app/go_src` relies on this library (`libprocessor.so`) via `cgo`. Currently, compiling the Go service fails because it cannot find the shared library at link time, and running it fails at runtime. Modify the build process, `CMakeLists.txt`, or Go files so that `go build` successfully links the library and the resulting binary can run.

2. **Implement the Go gRPC Service**:
   In `/home/user/app/go_src`, you will find the `main.go` skeleton and a protobuf definition in `/home/user/app/proto/processor.proto`.
   - Generate the Go protobuf bindings.
   - Implement the `ProcessorService` gRPC server in `main.go`, listening on `127.0.0.1:50051`.
   - **Rate Limiting**: Implement rate limiting using Redis (running on `127.0.0.1:6379`). Each `client_id` is allowed a maximum of 3 requests per second. Use a simple fixed-window counter in Redis (key format: `rate:{client_id}:{unix_timestamp_seconds}`). If a client exceeds 3 requests in the same second, return a gRPC error with code `codes.ResourceExhausted` (HTTP 429).
   - **FFI/cgo Integration**: If the request is allowed, call the C function `process_data(const char* input)` from `libprocessor.so` via `cgo`. Pass `input_data` from the request. The C function returns a heap-allocated string; your Go code MUST free this memory to prevent leaks. Return the string in the gRPC response.

3. **Orchestrate the Test Environment**:
   Modify `/home/user/app/start.sh` so that when executed, it:
   - Starts Redis.
   - Builds and starts the Go gRPC service in the background.
   - Starts the provided Python Flask gateway (`/home/user/app/python_gateway/app.py`) in the background, which listens on `127.0.0.1:8080`.
   - The script should exit with code 0 while leaving the services running.

Make sure your implementation is robust. You can test the end-to-end flow by running `./start.sh` and sending POST requests to `http://127.0.0.1:8080/process` with JSON body `{"client_id": "test1", "input_data": "hello"}`.