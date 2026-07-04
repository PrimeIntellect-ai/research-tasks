You are a cloud architect simulating a staged migration of a legacy API to a new microservice architecture. You are working in a non-root environment in `/home/user`. 

Two backend services have already been written for you:
1. `/home/user/backend_v1.go` (legacy API, listens on 127.0.0.1:8081)
2. `/home/user/backend_v2.go` (new API, listens on 127.0.0.1:8082)

Your task is to write a Go-based reverse proxy and a deployment script to manage these services. Because of a previous issue where the proxy crashed on startup due to missing backend dependencies, you must implement a robust startup synchronization mechanism.

Please complete the following steps:

1. **Write the Reverse Proxy (`/home/user/proxy.go`)**:
   - Write a Go program that starts an HTTP server listening on `127.0.0.1:8080`.
   - **Startup Dependency Wait**: Before starting the HTTP server, the proxy must continuously read the file `/home/user/startup.txt`. It must wait (block/loop) until it finds *both* the string `v1_ready` and `v2_ready` on separate lines in that file. Only after both strings are present should the server bind to port 8080.
   - **Staged Deployment Routing**: The proxy should inspect incoming requests. If a request contains the HTTP header `X-API-Version: v2`, route the request to the v2 backend at `http://127.0.0.1:8082`. Otherwise, default to routing the request to the legacy v1 backend at `http://127.0.0.1:8081`. Return the exact response from the backend to the client.
   - **Logging**: For every request processed, append a single line to `/home/user/proxy.log` in the exact format: `<version_routed_to> <request_path>`. For example: `v1 /api/users` or `v2 /api/users`.

2. **Write the Deployment Script (`/home/user/deploy.sh`)**:
   - Create a bash script that coordinates the deployment.
   - Clear or create `/home/user/startup.txt` and `/home/user/proxy.log`.
   - Ensure the proxy log file `/home/user/proxy.log` has strict ACL/permissions: exactly `640` (read/write for owner, read for group, no permissions for others).
   - Compile and start `/home/user/proxy.go` in the background.
   - Compile and start `/home/user/backend_v1.go` in the background.
   - Append the string `v1_ready` to `/home/user/startup.txt`.
   - Compile and start `/home/user/backend_v2.go` in the background.
   - Append the string `v2_ready` to `/home/user/startup.txt`.
   - The script must leave the three Go binaries running in the background.

3. **Execute the Deployment**:
   - Run `/home/user/deploy.sh` and ensure the proxy is successfully listening on port 8080 and appropriately routing traffic. 

Do not rely on `systemd` or root privileges. Ensure you use absolute paths for file reading/writing in your Go code (e.g., `/home/user/startup.txt`).