You are an open-source maintainer reviewing a broken Pull Request for a Web Security microservices project located in `/home/user/app`. The project consists of three cooperating services: an API Gateway (REST), an Auth Service (gRPC), and a Backend Service (gRPC).

The contributor attempted to introduce a custom security policy expression language evaluator into the Auth Service to allow dynamic, attribute-based access control (ABAC). However, the PR is broken on several fronts:

1. **Protobuf & Dependencies**: The gRPC protobuf definition at `/home/user/app/proto/auth.proto` is missing the `map<string, string> attributes` field (as field number 3) in the `CheckRequest` message. The Go module in `/home/user/app/auth` has broken dependencies.
   - You must fix the protobuf definition and regenerate the Go gRPC stubs using `protoc`.
   - You must fix the `go.mod` file and resolve dependencies in the `auth` directory.

2. **Expression Parser Implementation**: The contributor wrote a buggy parser/evaluator in `/home/user/app/auth/parser.go`. It fails on precedence and specific equality checks.
   - We require the new Go evaluator to be **bit-exact equivalent** to our legacy reference evaluator, which is available as a compiled binary at `/opt/oracle/evaluator`.
   - You must fix the Go code and produce a standalone CLI binary at `/home/user/app/auth/auth_eval`.
   - The CLI binary must take exactly two arguments: the expression string, and a JSON string of attributes. It must print exactly `true` or `false` to stdout. For example: `/home/user/app/auth/auth_eval "role == 'admin' && method == 'POST'" '{"role":"admin", "method":"POST"}'`

3. **Service Composition & Routing**: The microservices fail to boot and route traffic properly. 
   - The Gateway expects Auth to be on port 50051 and Backend on 50052.
   - Fix the startup script at `/home/user/app/start.sh` and the gateway configuration file at `/home/user/app/gateway/config.yaml` to wire the ports and hostnames correctly.
   - Once running, a request to `http://localhost:8080/secure-data` with attributes that satisfy the hardcoded policy in the Gateway should correctly flow through Auth and return a 200 OK from the Backend.

Your final deliverables are:
- The compiled `auth_eval` binary at `/home/user/app/auth/auth_eval` that matches the oracle's logic.
- A functional `start.sh` that brings up all three services on their correct ports (Gateway: 8080, Auth: 50051, Backend: 50052) such that they can process end-to-end requests.