You are a release manager preparing a telemetry processing pipeline for software deployments. We have a multi-service architecture located in `/home/user/app/` that processes incoming release telemetry.

The system consists of:
1. A Redis instance (already running on `127.0.0.1:6379`).
2. A Go-based reverse proxy that handles concurrency and routes requests.
3. A C-based processing backend that analyzes semantic versions and stores telemetry in Redis.

Your task is to fix the backend implementation, configure the proxy, and start the services so the end-to-end flow works.

Step 1: Fix the C Processing Backend
The source code for the backend is in `/home/user/app/backend/server.c`. It is a simple TCP server that listens for incoming JSON payloads from the proxy.
Currently, the semantic version comparison logic is missing. You need to implement the function `int is_valid_release(const char* version)`.
- The function should parse a semantic version string (e.g., "1.2.3" or "v2.1.0"). Note that the "v" prefix is optional and should be ignored if present.
- It must return `1` if the version is `>= 2.0.0`, and `0` otherwise.
- The server receives messages formatted precisely as: `<version>|<data_string>`.
- If the version is valid, the server should append `<data_string>` to a Redis list named `releases:valid`.
- If the version is invalid, append to `releases:invalid`.
The `hiredis` library is installed on the system. Update `/home/user/app/backend/Makefile` to properly link against `-lhiredis` and compile the backend. Run `make` to build the `backend_server` executable.

Step 2: Configure the Go Reverse Proxy
The Go proxy is already compiled at `/home/user/app/proxy/proxy_server`. It reads routing rules from `/home/user/app/proxy/config.json`.
Modify `config.json` to route all incoming HTTP traffic to your C backend.
- The Go proxy must listen on `127.0.0.1:8080`.
- It must forward the raw body of POST requests to the C backend via a plain TCP connection on `127.0.0.1:8081`.
- The `config.json` requires the fields: `{"listen_addr": "127.0.0.1:8080", "backend_addr": "127.0.0.1:8081"}`.

Step 3: Start the Services
Start the compiled C `backend_server` (listening on 8081) and the Go `proxy_server` in the background. Keep them running so that our automated test suite can verify the pipeline.

The automated test will send HTTP POST requests to `http://127.0.0.1:8080` containing payloads like `v2.1.5|deployment_A` and `1.9.9|deployment_B`, and will verify that Redis correctly categorizes them.