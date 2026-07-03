You are an engineer setting up a polyglot build system and implementing a web security service from scratch.

Your task is to complete the setup in `/home/user/project`. 
There are multiple phases:

Phase 1: Dependencies
Install the required tools for Go and protobufs. You do not have root access, so install local binaries. 
Ensure you have `protoc` and the Go plugins (`protoc-gen-go`, `protoc-gen-go-grpc`) installed and available in your PATH.

Phase 2: Protobuf Definition
Create a protobuf file at `/home/user/project/proto/security.proto` with:
- Syntax: `proto3`
- Package: `security`
- Go package option: `security/pb`
- A service named `SecurityAnalyzer`.
- An RPC method `AnalyzeLogs` that takes an `AnalyzeRequest` and returns an `AnalyzeResponse`.
- `AnalyzeRequest` has one field: `repeated string logs = 1;`
- `AnalyzeResponse` has one field: `repeated string malicious_ips = 1;`

Phase 3: The Build System
Create a `Makefile` at `/home/user/project/Makefile` with the following targets:
- `rules`: Runs `python3 python/generate.py` (which we provide) to generate `rules.json` in the project root.
- `proto`: Compiles `proto/security.proto` into `/home/user/project/go/pb/`. Ensure paths resolve correctly so the generated files end up in the `pb/` directory under `go/`.
- `build`: Depends on `rules` and `proto`. Builds the Go binary and outputs it to `/home/user/project/bin/server`.
- `test`: Depends on `proto` and `rules`. Runs `go test ./...` in the `go/` directory.

Phase 4: Service Implementation
Initialize a Go module named `security` in `/home/user/project/go`. Add required gRPC and protobuf dependencies.
Create `/home/user/project/go/server.go`. Implement the `SecurityAnalyzerServer`:
- It must read `/home/user/project/rules.json` (a JSON array of string paths, e.g., `["/.git", "/admin"]`).
- `AnalyzeLogs` receives a list of log strings. Each string is formatted exactly as: `"<IP> <METHOD> <PATH>"` (e.g., `"192.168.1.1 GET /.git"`).
- You must use Go concurrency (goroutines and channels) to process the logs in parallel.
- A log is considered malicious if its `<PATH>` is exactly present in the loaded `rules.json`.
- Extract the IPs from malicious logs, remove duplicates, sort them alphabetically, and return them in `malicious_ips` in the response.

To complete the task:
1. Ensure the `Makefile` runs properly.
2. Run `make test` and pipe the output to `/home/user/test_report.txt`.
3. Run `make build`.

We have placed `python/generate.py` and `go/server_test.go` in `/home/user/project`. Do not modify `go/server_test.go`.