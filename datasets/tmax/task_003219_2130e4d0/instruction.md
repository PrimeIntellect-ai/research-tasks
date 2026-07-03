You are tasked with fixing and deploying a local "Data Integrity Verification Node" (DIVN). The project consists of a WebSocket server written in C that calculates a Fletcher-16 checksum of incoming binary messages and sends the checksum back. 

Currently, the server has three issues:
1. The checksum function is incomplete.
2. It has a memory leak.
3. It needs a reverse proxy to handle incoming client connections.

Here are your instructions:

1. **Fix the C Server code**: 
   The source code is located at `/home/user/divn/server.c`. 
   - Implement the `compute_fletcher16` function (standard Fletcher-16 algorithm returning a `uint16_t`).
   - Identify and fix the memory leak inside the `on_message_received` callback. (A buffer is allocated but never freed).
   
2. **Compile the Server**:
   Navigate to `/home/user/divn/` and compile the server. A `Makefile` is provided. The output executable will be named `divn_server` and listens on `127.0.0.1:9000`.

3. **Configure Nginx as a Reverse Proxy**:
   Create an Nginx configuration file at `/home/user/nginx.conf`.
   - It must listen on port `8080`.
   - It must proxy all requests to `http://127.0.0.1:9000`.
   - It must include the correct headers to support WebSocket connection upgrades (`Upgrade` and `Connection` headers).
   - Set the Nginx `error_log` to `/home/user/nginx_error.log` and `pid` to `/home/user/nginx.pid` so it can run without root. Include `events {}` block.

4. **Run the Services**:
   - Start Nginx in the background: `nginx -c /home/user/nginx.conf -p /home/user/`
   - Start the C server in the background using valgrind to verify no memory leaks occur:
     `valgrind --leak-check=full --log-file=/home/user/valgrind.log /home/user/divn/divn_server &`

Leave the proxy and server running so that our automated test script can connect to `ws://127.0.0.1:8080`, send a test payload, verify the Fletcher-16 checksum response, and then shut down the server to inspect `/home/user/valgrind.log` for memory leaks.