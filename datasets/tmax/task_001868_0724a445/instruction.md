You are a developer tasked with organizing a messy web security project, fixing a custom checksum algorithm, and correctly composing its microservices. 

The project files are currently dumped in `/home/user/project/`. Your goals are:

1. **Project Organization (Go)**:
   - Move the main API entrypoint `api.go` to `cmd/secapi/main.go`.
   - Move `secsum.go` to `pkg/secsum/secsum.go`.
   - Update the import paths in the Go files accordingly so the project compiles.
   - Compile the standalone CLI version of the checksum tool (currently `cli.go`) into `/home/user/project/bin/secsum_cli`. You should move `cli.go` to `cmd/cli/main.go` and build it.

2. **Fix the Checksum Algorithm**:
   - The Go implementation in `secsum.go` is buggy. It's supposed to compute a secure web token signature.
   - We have an old Rust implementation in `/home/user/project/legacy/secsum.rs` that has a known borrow-checker/lifetime bug but structurally shows the correct mathematical logic. 
   - A compiled oracle binary of the correct logic is available at `/opt/oracle/secsum`.
   - Fix the Go `secsum.go` implementation so its output matches the oracle *exactly* for any string input. The CLI you built (`bin/secsum_cli <string>`) must output the exact same string as `/opt/oracle/secsum <string>`.

3. **Multi-Service Composition**:
   - The system consists of three services: Nginx (port 8080), the Go API (port 8000), and a Redis cache (port 6379).
   - Edit `/home/user/project/nginx.conf` so that requests to `/api/` are proxy-passed to the Go API.
   - Create a `.env` file in `/home/user/project/` containing the correct configuration for the Go API to connect to Redis (`REDIS_ADDR=127.0.0.1:6379`).
   - Create an executable shell script at `/home/user/project/start.sh` that starts the Redis server in the background, starts the Go API (`cmd/secapi/main.go`) in the background, and starts Nginx using the local `nginx.conf`. 

To complete the task:
- Ensure `/home/user/project/bin/secsum_cli` exists and correctly implements the algorithm.
- Ensure `/home/user/project/start.sh` successfully brings up the stack so that `curl http://127.0.0.1:8080/api/sign?data=hello` returns the correct checksum from the Go API.