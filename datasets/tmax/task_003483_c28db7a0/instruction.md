You are a cloud architect tasked with migrating a legacy authentication and routing service to a modern, cloud-native API Gateway model. 

We have a legacy authentication daemon provided as a stripped, undocumented binary located at `/app/legacy_auth`. Your task is to write a Go-based reverse proxy that sits in front of it, orchestrate the directory structure it expects, and create a deployment script to run the environment.

**Step 1: Legacy Daemon Environment Setup**
The `/app/legacy_auth` binary expects a specific directory structure to function.
- It unconditionally reads its configuration from `/home/user/legacy_system/active/secret.txt`.
- You must create a directory `/home/user/configs/v2_migrated/` containing a file named `secret.txt`. Write the string `cloud_migration_2024` into this file.
- You must use directory symlinks so that `/home/user/legacy_system/active` points to `/home/user/configs/v2_migrated`.
- When started, `/app/legacy_auth` binds to `127.0.0.1:9000`. It accepts raw TCP connections, reads a single line of text, and responds with either `VALID\n` or `INVALID\n`. 

**Step 2: The Go Reverse Proxy**
Write a Go reverse proxy in `/home/user/gateway/main.go` that does the following:
- Listens for HTTP requests on `0.0.0.0:8080`.
- For every incoming HTTP request, extracts the `X-Auth-Token` header.
- Opens a TCP connection to the legacy daemon at `127.0.0.1:9000`, sends the token (appended with a newline `\n`), and reads the response.
- If the legacy daemon responds with `VALID\n`, the Go proxy must forward the original HTTP request to our backend API located at `127.0.0.2:8081` (you do not need to build the backend API, the automated verifier will start it). The proxy should transparently return the backend's response to the client.
- If the legacy daemon responds with `INVALID\n` (or if it fails to connect), the Go proxy must intercept the request and return an HTTP `401 Unauthorized` status code with the JSON body `{"error": "unauthorized"}`.

**Step 3: Metrics Endpoint**
The Go proxy must also expose a raw TCP metrics endpoint on `0.0.0.0:8082`. When a client connects to this port and sends the exact string `STATS\n`, the proxy must respond with the total number of successful (VALID) authorizations it has processed since it started, in the format `SUCCESS_COUNT: <number>\n`, and then close the connection.

**Step 4: Deployment Pipeline**
Create a deployment script at `/home/user/deploy.sh` that:
1. Compiles the Go reverse proxy.
2. Creates the necessary directory structures and symlinks for the legacy daemon.
3. Starts the `/app/legacy_auth` daemon in the background.
4. Starts the Go reverse proxy in the background.
5. Exits with code 0 once both processes are running and listening on their respective ports.

Ensure your `deploy.sh` script is executable. You may interactively run the legacy binary to deduce its behavior and test your proxy before finalizing the deployment script.