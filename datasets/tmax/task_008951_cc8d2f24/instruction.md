You are a container specialist managing a custom microservice deployment. Because you are operating in an unprivileged user space (without root access), standard tools like `iptables` or systemd are unavailable. You must implement the routing, load balancing, and process management entirely in user space using Go and Bash.

Your objective is to complete the following setup:

**Phase 1: Environment & Timezone Configuration**
1. Add an environment variable `APP_TIMEZONE="Asia/Tokyo"` to `/home/user/.bashrc`. 
2. Ensure that any processes you spawn in your final script source this profile so the environment variable is loaded.

**Phase 2: Backend Microservices (Go)**
1. Write a Go program at `/home/user/backend.go`. It should accept a port number as a command-line argument.
2. It must start an HTTP server on `127.0.0.1:<port>`.
3. For any incoming GET request, it should return the exact string: `Backend responding from port <port>`.

**Phase 3: Reverse Proxy & Load Balancer (Go)**
1. Write a Go program at `/home/user/lb.go`.
2. It must act as an HTTP reverse proxy and load balancer listening on `127.0.0.1:8080`.
3. It must strictly round-robin incoming requests between two backend addresses: `127.0.0.1:8081` and `127.0.0.1:8082`.
4. It must read the `APP_TIMEZONE` environment variable. For every response sent back to the client, it must inject an HTTP header named `X-Forwarded-Time` containing the current time in that specific timezone, formatted strictly as an RFC3339 string (e.g., `2023-10-25T14:30:00+09:00`).

**Phase 4: User-Space Port Forwarding (Go)**
Since you lack firewall/iptables permissions, implement port forwarding via a TCP proxy in Go.
1. Write a Go program at `/home/user/forwarder.go`.
2. It must listen for TCP connections on `127.0.0.1:9090` and transparently pipe all raw bytes to and from `127.0.0.1:8080` (the load balancer).

**Phase 5: Robust Orchestration Script (Bash)**
1. Write a Bash script at `/home/user/run_system.sh`.
2. The script must be robust: it should source `/home/user/.bashrc`, compile the three Go files, and start two backend instances (ports 8081 and 8082), the load balancer (port 8080), and the forwarder (port 9090) in the background.
3. Implement a health check loop that waits (with a timeout) until `127.0.0.1:9090` is accepting connections and successfully returning HTTP responses.
4. Once healthy, the script must make exactly 4 `curl -i -s http://127.0.0.1:9090/` requests.
5. Append the raw output (headers and body) of these 4 requests to `/home/user/test_results.log`.
6. Make sure `/home/user/run_system.sh` is executable. You do not need to keep the script running after the 4 requests are logged (you may kill the background processes or leave them running, it doesn't matter).

Ensure your code handles errors gracefully and correctly manages concurrency in the proxy/forwarder. Do not use any third-party Go libraries (only the standard library).