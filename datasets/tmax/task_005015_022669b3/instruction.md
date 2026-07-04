You are an engineer tasked with porting a legacy security filter tool to work securely in a new containerized infrastructure. 

A legacy WAF (Web Application Firewall) engine has been provided to you as a stripped binary located at `/app/waf_engine`. Unfortunately, the original source code and documentation have been lost. The binary is known to read from standard input and write filtered output to standard output, but if executed directly, it crashes or returns an error. 

Your objectives are:

1. **Analyze the Binary**: Reverse-engineer `/app/waf_engine` to determine the specific environment variable and command-line argument it requires to run successfully without crashing.
2. **Create a C TCP Wrapper**: Write a C program at `/home/user/backend.c` and compile it to `/home/user/backend`. This program must:
   - Listen for incoming raw TCP connections on `127.0.0.1:9090`.
   - Upon receiving a line of text (up to a newline) from a client, spawn the `/app/waf_engine` process with the correct environment variables and arguments you discovered.
   - Feed the client's text to the engine's standard input.
   - Read the engine's standard output and send it back to the TCP client.
   - Cleanly close the connection (or handle multiple messages, but handling one request per connection is acceptable).
3. **WebSocket Translation**: The frontend requires a WebSocket interface. Since your C backend speaks raw TCP, use a tool like `websockify` to expose your TCP backend as a WebSocket service listening on `127.0.0.1:9091`.
4. **Reverse Proxy & Authentication**: Configure and start `nginx` to act as the public gateway.
   - Listen on `0.0.0.0:8080`.
   - Route requests for the path `/api/waf` to your local WebSocket service on port 9091.
   - Ensure the Nginx configuration properly handles the HTTP to WebSocket upgrade process (passing `Upgrade` and `Connection` headers).
   - Protect the `/api/waf` endpoint by requiring the client to provide the HTTP header: `Authorization: Bearer WAF-2024-SEC`. If this header is missing or incorrect, return a 401 or 403 status code.

Ensure all services (your compiled C backend, websockify, and nginx) are running in the background before you declare the task complete. Do not alter the `/app/waf_engine` binary. You are running as the `user` account and have access to `sudo` for installing packages like `nginx`, `websockify`, `gdb`, `strace`, etc.