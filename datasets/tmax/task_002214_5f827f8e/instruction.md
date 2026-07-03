You are a network engineer troubleshooting connectivity in a high-throughput environment. We need to set up a minimal, high-performance web server simulating an endpoint, along with its required directory structures and configuration environment. 

You have been provided with a stripped benchmarking binary at `/app/bench`. 

Please perform the following steps:

1. **Certificate and Directory Structure:**
   - Create directories `/home/user/certs` and `/home/user/www`.
   - Generate a self-signed RSA TLS certificate (`server.crt`) and private key (`server.key`) in `/home/user/certs`.
   - Create symlinks `/home/user/certs/active.crt` pointing to `server.crt`, and `/home/user/certs/active.key` pointing to `server.key`.
   - Create a file `/home/user/www/target.html` containing exactly the string `NETWORK_OK`.
   - Create a symlink `/home/user/www/index.html` pointing to `target.html`.

2. **Environment Variable Setup:**
   - Append the following exports to `/home/user/.bashrc`:
     `export WWW_PORT=8080`
     `export CERT_PATH=/home/user/certs/active.crt`

3. **High-Performance C Web Server:**
   - Write a C program at `/home/user/server.c` that listens for TCP connections on port 8080.
   - For every incoming connection, it should immediately respond with a valid HTTP 1.1 200 OK response containing the contents of `/home/user/www/index.html` as the body, and then close the connection. (You do not need to implement TLS in the C server itself; assume a reverse proxy handles TLS termination using the certs you generated).
   - Compile this program to `/home/user/server`.
   - The server must be highly efficient. We will use the provided `/app/bench` utility to benchmark your server. It must sustain a throughput of at least 5000 requests per second.

Do not start the server in a blocking way as your final action, as the automated tests will start it and run the benchmark. Just ensure the binary is compiled and ready at `/home/user/server`.