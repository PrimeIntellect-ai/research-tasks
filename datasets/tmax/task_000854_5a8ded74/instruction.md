You are a systems programmer taking over a legacy data processing microservice. The core logic of this service is embedded in a pre-compiled C shared library, `libtransform.so`, for which the original source code has been lost. 

Your objective is to build a new backend service that wraps this library, and configure a reverse proxy to expose it.

Here is the current state of your workspace in `/home/user/app`:
- `/home/user/app/lib/libtransform.so`: The compiled shared library.
- `/home/user/app/lib/transform.h`: The header file found alongside the library. (Warning: Notes from the previous developer suggest this header might be outdated and not exactly match the compiled ABI in the `.so` file. You will need to analyze the binary to determine the correct function symbol and signature).
- `/home/user/app/nginx/nginx.conf`: A skeleton Nginx configuration file.

Your tasks:
1. **Analyze the Shared Library:** Inspect `libtransform.so` to determine the actual function name and its parameters. The function performs a simple string transformation.
2. **Build the Backend Service:** Write a service in any language of your choice (Python, Go, Node.js, C++, Rust, etc.) that loads this shared library and correctly calls the transformation function via FFI.
3. **Multi-Protocol Endpoints:** Your backend service must expose two endpoints:
   - **HTTP REST:** Listen on `127.0.0.1:9000`. Expose a `POST /process` endpoint. The request body will contain raw text. The response should be the raw transformed text returned by the C library.
   - **TCP Health Check:** Listen on `127.0.0.1:9001`. It must accept raw TCP connections. If the client sends the string `"PING\n"`, it must immediately reply with `"PONG\n"` and close the connection.
4. **Reverse Proxy:** Edit `/home/user/app/nginx/nginx.conf` so that Nginx listens on `0.0.0.0:8080`. It must route all incoming HTTP traffic matching the path `/api/process` to your backend's `POST /process` endpoint (at `127.0.0.1:9000`). Nginx must strip the `/api` prefix before forwarding (i.e., forward to `/process`).
5. **Start Services:** Start both your backend service in the background and Nginx (using your config file). Ensure they are running and listening on the specified ports.

To complete the task, ensure both Nginx and your backend are fully running, and exit. An automated verifier will test the `8080` HTTP endpoint and the `9001` TCP endpoint.