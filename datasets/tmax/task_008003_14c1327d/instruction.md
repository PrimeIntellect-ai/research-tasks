You are an AI assistant helping a build engineer manage build artifacts and automation. We are building a system that allows developers to trigger builds of C projects via an HTTP API, stream logs over WebSockets, and query the build status via gRPC. 

We have a partially completed workspace. You need to fix a broken C project artifact, and then repair and run the Rust build-orchestration server.

**Task Requirements:**

**Phase 1: Fix the C Project**
There is a C project located in `/home/user/artifact/src`.
1. The `Makefile` is broken (it fails to build). Fix any syntax errors (e.g., standard Makefile tab rules).
2. The `main.c` file contains a compilation error. Fix the C code so that it cleanly compiles and simply prints "Artifact Built" to standard output.
3. Ensure that running `make` in `/home/user/artifact/src` successfully produces an executable named `app`.

**Phase 2: Fix the Rust Server**
A Rust server scaffold is located in `/home/user/artifact-server`. It uses `axum` for HTTP/WebSockets and `tonic` for gRPC. It has a few intentional bugs you must fix:
1. **URL Routing**: In `/home/user/artifact-server/src/main.rs`, the route for triggering a build is misconfigured. It should accept `POST` requests at `/build/{job_id}`. Update the axum routing and handler signature to correctly extract the `job_id` path parameter.
2. **gRPC Service**: In `/home/user/artifact-server/src/grpc.rs`, the `GetStatus` RPC is currently returning an `UNIMPLEMENTED` status. Modify it so that it returns a `StatusResponse` with the `status` field set to `"COMPLETED"` for any `job_id` it receives.

**Phase 3: Run and Verify**
1. Compile and run the Rust server (`cargo run` in `/home/user/artifact-server`). It will bind HTTP to `0.0.0.0:8080` and gRPC to `0.0.0.0:50051`.
2. While the server is running, use `curl` to trigger the build endpoint:
   `curl -X POST http://localhost:8080/build/job123`
   Save the exact output of this command to `/home/user/http_response.log`.
3. Use `grpcurl` (which is installed on the system) to query the gRPC endpoint:
   `grpcurl -plaintext -d '{"job_id": "job123"}' localhost:50051 build.BuildService/GetStatus`
   Save the exact output of this command to `/home/user/grpc_response.log`.

You are completely successful when the C project builds cleanly, the Rust server runs without errors, and the two log files contain the expected successful responses.