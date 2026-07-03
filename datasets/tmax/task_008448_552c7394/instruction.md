You are helping me refactor some legacy scripts used for organizing project files. We have an old Python script that scans a directory, calculates file hashes, and identifies duplicate files. We want to port this logic to Go and expose it as a gRPC service so it can be integrated into our larger file management system.

Here is the current state of the workspace:
* The old Python script is located at `/home/user/project/legacy/dedup.py`. You can read it to understand the exact algorithmic requirements (e.g., hash algorithm used, minimum file size ignored, traversal rules).
* There is a test directory with sample files at `/home/user/project/test_data/`.

Your task:
1. **gRPC and Protobuf Design**:
   Create a protobuf definition at `/home/user/project/proto/fileorg.proto`.
   It must define a package `fileorg` and a service `FileOrganizer`.
   The service should expose an RPC `FindDuplicates` that takes a `DuplicateRequest` and returns a `DuplicateResponse`.
   `DuplicateRequest` must contain a single string field: `directory_path`.
   `DuplicateResponse` must contain a repeated `DuplicateGroup` field named `groups`.
   `DuplicateGroup` must contain a string field `hash` and a repeated string field `file_paths`.

2. **Code Translation (Python to Go)**:
   Create a Go module in `/home/user/project/go_server/` named `fileorg`.
   Generate the Go gRPC code from your proto file into `/home/user/project/go_server/pb/`.
   Implement the gRPC server in Go (`/home/user/project/go_server/main.go`). It should accurately translate the deduplication logic from `dedup.py`. The server should listen on `localhost:50051`.
   *Note: Ensure the resulting duplicate groups only contain hashes that have 2 or more files, and sort the `file_paths` alphabetically within each group.*

3. **Client & Integration Testing**:
   Create a Go test file `/home/user/project/go_server/server_test.go` that tests your gRPC server against the `/home/user/project/test_data/` directory.
   Additionally, write a standalone Go CLI client at `/home/user/project/client/main.go` that connects to the server at `localhost:50051`, requests duplicates for `/home/user/project/test_data/`, and writes the raw response to `/home/user/project/duplicates.json` (just marshal the response to JSON using `encoding/json` or the `protojson` package).

4. **Execution Script**:
   Create a bash script at `/home/user/project/run.sh` that:
   - Builds the Go server and client.
   - Starts the server in the background.
   - Runs the Go tests (`go test`).
   - Runs the client to generate `/home/user/project/duplicates.json`.
   - Gracefully shuts down the background server.
   Make sure the script is executable (`chmod +x`).

The Go compiler, `protoc`, and necessary Go protoc plugins are already installed on the system. You can format the JSON output however the standard Go JSON/protojson marshaler does it.