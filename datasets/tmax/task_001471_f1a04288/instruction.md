You are a network security engineer tasked with setting up a secure inspection gateway and creating a traffic modification tool.

Your environment contains a set of services located under `/app/`:
1. A backend data API running on `127.0.0.1:8080`.
2. An Nginx secure gateway configuration directory at `/app/nginx/`.
3. Certificates located at `/app/certs/`.

There are two main objectives:

**Objective 1: Gateway Configuration (Multi-Service)**
You must configure the Nginx gateway to act as an mTLS-terminating reverse proxy.
1. Edit `/app/nginx/nginx.conf` so that Nginx listens on `127.0.0.1:8443` with SSL enabled.
2. Use `/app/certs/server.crt` and `/app/certs/server.key` for the server certificate.
3. Enable mutual TLS (mTLS) by requiring client certificates verified against `/app/certs/ca.crt`.
4. Forward all valid requests to the backend API at `http://127.0.0.1:8080`.
5. Pass the client certificate's Subject Common Name (CN) to the backend API using the HTTP header `X-Client-CN`.
6. Ensure the Nginx service is running and correctly configured. You can start/reload it using the provided script `/app/start_services.sh`.

**Objective 2: Traffic Modification Tool (Go)**
You must write a Go program at `/home/user/traffic_modifier.go` and compile it to `/home/user/traffic_modifier`.
This program will be used to automatically analyze and modify raw HTTP requests for security auditing.
The program must:
1. Read a raw HTTP/1.x request from `stdin` until EOF.
2. Parse the HTTP request.
3. Read the client certificate located at `/app/certs/client.crt`, parse its X.509 structure, and extract its Subject Common Name (CN).
4. Modify the HTTP request based on the following rules:
   - Add a new header `X-Cert-CN` with the value of the extracted CN.
   - Inspect the `Cookie` header. If a cookie named `legacy_auth` exists and its value is exactly `1`, inject a new header: `X-Legacy-Bypass: true`.
   - Modify the `User-Agent` header by appending the string ` - inspected` to its existing value. If it doesn't exist, set it to `inspected`.
   - Exploit payload delivery: If the `Host` header starts with the exact string `internal-`, modify the request URI path by prepending `/admin/debug` to the existing path (e.g., `/api/data` becomes `/admin/debug/api/data`).
5. Write the modified raw HTTP request to `stdout` in the standard format (matching the standard `net/http` request serialization format, e.g., using `req.Write(os.Stdout)`).

Ensure your Go program precisely matches this behavior, as it will be rigorously tested against a variety of inputs.