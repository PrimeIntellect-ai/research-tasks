You are a deployment engineer tasked with rolling out a backend update. A user-space Nginx reverse proxy is configured, but it is currently returning a `502 Bad Gateway` error because the new backend service is not running and listening on the expected socket.

Your objectives:
1. **Analyze Nginx Config**: Inspect the Nginx configuration file located at `/home/user/nginx/nginx.conf`. Identify the Unix Domain Socket path it uses as the upstream backend, and the local port Nginx is configured to listen on.
2. **Develop the Rust Backend**: A skeleton Cargo project exists at `/home/user/backend`. Write a dependency-free Rust application in `/home/user/backend/src/main.rs` that uses `std::os::unix::net::UnixListener` to bind to the exact socket path expected by Nginx. The application must accept connections, read the incoming HTTP request (a basic `Read` into a buffer is sufficient), and write a valid raw HTTP response: `HTTP/1.1 200 OK` with the body exactly matching `Deploy v2 OK`. (Remember to include proper `\r\n` line endings and `Content-Length`).
3. **Run the Services**: 
   - Compile and run your Rust backend in the background.
   - Start Nginx in the background using the provided configuration: `nginx -c /home/user/nginx/nginx.conf -g 'daemon off;' &`
4. **Establish an SSH Tunnel**: Expose the application for external testing by setting up a local SSH port forward. Forward local port `8888` to the port Nginx is listening on. Use the SSH server at `localhost` and the pre-existing private key at `/home/user/.ssh/id_rsa` (e.g., `ssh -i /home/user/.ssh/id_rsa -N -L 8888:127.0.0.1:<NGINX_PORT> user@localhost &`).
5. **Verification**: Once the tunnel is up, test the deployment by querying the forwarded port: `curl http://127.0.0.1:8888/` and save the exact output of this curl command to `/home/user/deploy_test.txt`.

Ensure your Rust server correctly cleans up any stale socket files before binding to prevent `Address already in use` errors.