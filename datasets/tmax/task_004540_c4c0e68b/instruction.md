You are a network security engineer tasked with inspecting and securing traffic for a legacy internal API. The architecture consists of a frontend reverse proxy, a custom C++ security inspection proxy, and a backend Python API. 

Currently, the services are not properly glued together, TLS is missing, and the C++ proxy lacks the logic to redact sensitive data and block basic automated vulnerability scans. 

Your task is to complete the multi-service setup and implement the security inspection logic.

**System Architecture:**
1. **Nginx Reverse Proxy**: Should listen on HTTPS port 8443, terminate TLS, and forward plain HTTP traffic to the C++ Proxy.
2. **C++ Security Proxy**: Should listen on HTTP port 8080. It must inspect headers/cookies, apply security rules, and forward valid traffic to the Backend API.
3. **Backend API**: Runs on HTTP port 8081 (already implemented in `/app/backend/server.py`).

**Step 1: TLS Management & Nginx Configuration**
* Create a local directory `/home/user/nginx_setup/`.
* Generate a self-signed RSA 2048-bit TLS certificate (`server.crt`) and private key (`server.key`) in `/home/user/nginx_setup/`. Use `CN=localhost`.
* A skeleton Nginx configuration exists at `/app/nginx/nginx.conf`. Copy it to `/home/user/nginx_setup/nginx.conf`.
* Modify `/home/user/nginx_setup/nginx.conf` so that it:
  - Listens on `127.0.0.1:8443` with SSL.
  - Uses the generated `server.crt` and `server.key`.
  - Proxies all requests (`location /`) to `http://127.0.0.1:8080`.
  - Configures `pid` and log files to write to `/home/user/nginx_setup/` so it can run without root privileges.

**Step 2: Implement C++ Security Proxy Logic**
A skeleton for the proxy is located at `/app/proxy/proxy.cpp`. It handles the TCP socket boilerplate, but the `inspect_and_modify_http` function is incomplete.
You must modify `/app/proxy/proxy.cpp` to implement the following rules:
1. **Vulnerability Scanning Prevention**: If the incoming HTTP request (headers or request line) contains the exact substring `UNION SELECT` or `<script>`, the proxy must NOT forward the request to the backend. Instead, it must immediately return an HTTP response: `HTTP/1.1 403 Forbidden\r\nContent-Length: 17\r\n\r\nMalicious payload`.
2. **Sensitive Data Redaction**: The backend expects cookies, but the `session_id` cookie must be redacted before it hits the backend. If the `Cookie:` header contains `session_id=<any alphanumeric string>`, you must replace the value with `REDACTED` (e.g., `Cookie: session_id=12345; user=admin` becomes `Cookie: session_id=REDACTED; user=admin`).

**Step 3: Build and Start Services**
* Compile your modified proxy: `g++ /app/proxy/proxy.cpp -o /home/user/proxy_server -std=c++11 -pthread`
* Start the backend API: `python3 /app/backend/server.py &`
* Start your C++ proxy: `/home/user/proxy_server &`
* Start Nginx as a non-root user using your config: `nginx -c /home/user/nginx_setup/nginx.conf -g 'daemon off;' &`

Make sure all services are running and correctly routing traffic from `https://127.0.0.1:8443` -> `8080` -> `8081`. The automated verifier will act as a client and send various HTTP requests to `https://127.0.0.1:8443` to test your TLS configuration, redaction, and vulnerability blocking.