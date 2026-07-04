You are a build engineer managing an artifact processing pipeline. We have a Node.js WebSocket server (`/home/user/server.js`) that emits artifact metadata, and a Go client (`/home/user/client.go`) that consumes these messages, parses them to extract the artifact names using a simple state machine, and processes them concurrently.

However, the Go client is currently failing to process the artifacts. It has two main issues:
1. **Concurrency bug**: The Go client deadlocks and never prints the processed artifacts. It uses goroutines and channels improperly.
2. **Parser bug**: The `parseArtifact` state machine in the Go client does not correctly extract the artifact name from the incoming message string. The expected format from the server is `[ARTIFACT] name:<name> | deps:<deps>;`.

Your tasks:
1. Debug and fix `/home/user/client.go` so it correctly extracts the artifact name (e.g., `core`, `utils`, `app`) and safely collects them concurrently without deadlocking. Ensure the processed names are printed to standard output in the format `Processed: <name>`.
2. Write an end-to-end test script at `/home/user/e2e.sh` (make it executable). The script should:
   - Start the Node.js server in the background.
   - Wait for 1 second to ensure the server is ready.
   - Run the Go client and save its standard output to `/home/user/output.log`.
   - Terminate the Node.js server background process.
   - Exit with a 0 status code.

Ensure your modifications to `client.go` only use standard Go libraries or the already imported `github.com/gorilla/websocket`.