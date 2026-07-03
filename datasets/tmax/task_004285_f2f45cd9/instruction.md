You are tasked with fixing and completing a local development environment for a new real-time chat architecture. The previous developer was migrating a backend service from a multi-file Rust project to Go, but left the Go project in a state that fails to compile due to syntax errors and incomplete routing logic. 

Your goals are to fix the Go service, implement a property-based test for its router, and correctly compose the services using Nginx and Redis.

**Environment Setup:**
Everything is located in `/home/user/app/`. There are three services that need to run concurrently:
1. **Redis**: Needs to run on `127.0.0.1:6379`.
2. **Go WebSocket Service**: Located in `/home/user/app/chat-server`. It must run on `127.0.0.1:9000`.
3. **Nginx Reverse Proxy**: Configuration located at `/home/user/app/nginx/nginx.conf`. It must listen on `127.0.0.1:8080`.

**Step 1: Fix the Go Project**
Navigate to `/home/user/app/chat-server`. The previous developer accidentally left some Rust-like syntax and unresolved imports in `router.go` and `main.go`.
- Fix the compilation errors.
- Implement the missing WebSocket upgrade logic in `router.go`. The endpoint must be accessible at `/ws/room/{room_id}` where `{room_id}` is an alphanumeric string.
- The service must require an authorization header: `Authorization: Bearer <token>`. The server should accept any connection where `<token>` equals `secret-chat-token-123`, and reject others with an HTTP 401.
- Upon successful connection, the server must echo back any received text message prefixed with `Room <room_id>: `.

**Step 2: Property-Based Testing**
In `/home/user/app/chat-server/router_test.go`, write a property-based test using Go's `testing/quick` package. 
- Create a function that tests the `ParseRoomID(path string) (string, error)` function (which you must implement/fix in `router.go`).
- The property test must verify that for any randomly generated alphanumeric string, `ParseRoomID("/ws/room/" + randomStr)` successfully extracts `randomStr`.
- Run the test and save its output to `/home/user/app/test_results.log`.

**Step 3: Service Composition**
- Edit `/home/user/app/nginx/nginx.conf` to proxy requests from `127.0.0.1:8080` to the Go service on `127.0.0.1:9000`.
- Ensure Nginx is configured to properly forward HTTP to WebSocket upgrades for the `/ws/` path.
- Start Redis, the Go service, and Nginx. Keep them running in the background.

When you are finished, write a file `/home/user/app/ready.txt` containing the word `DONE`.