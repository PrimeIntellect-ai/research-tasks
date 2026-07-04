You are an engineer tasked with porting a legacy Linux system check tool to work in a minimal container environment. The tool currently uses REST, but the backend has been migrated to a gRPC service. Because the container has strict networking rules, the tool must communicate with the backend via a local reverse proxy.

Your objectives:

1. **Protobuf Design & Reverse Engineering**
   There is a mock gRPC server running or ready to run at `/home/user/mock_server.py`. Inspect it to understand the service definition.
   Write the corresponding Protocol Buffers definition file at `/home/user/system.proto`. 
   The service name should be exactly what the Python server expects, and the syntax must be `proto3`.

2. **Reverse Proxy Configuration**
   The minimal container requires traffic to go through an Nginx reverse proxy.
   Create an Nginx configuration file at `/home/user/nginx.conf` that:
   - Runs in the foreground (daemon off)
   - Listens on port `8080` using HTTP/2
   - Forwards all gRPC traffic to the mock gRPC server listening on `127.0.0.1:50051` without TLS (plaintext).

3. **Diff and Patch Processing**
   The legacy Bash script is located at `/home/user/check_system.sh`.
   It currently makes a standard `curl` request to an old REST endpoint. 
   Generate a unified diff patch file at `/home/user/update.patch` that modifies `/home/user/check_system.sh` so that it instead uses `grpcurl` to call the `GetStatus` method of the gRPC service through the Nginx proxy (`localhost:8080`). 
   - You must use the `-proto /home/user/system.proto` and `-plaintext` flags with `grpcurl`.
   - Apply the patch to `/home/user/check_system.sh`.

4. **Testing and Execution**
   - Start the python mock server (`python3 /home/user/mock_server.py &`).
   - Start Nginx using your config (`nginx -c /home/user/nginx.conf &`).
   - Run the patched `/home/user/check_system.sh` and redirect its output to `/home/user/success.log`.

Ensure that the final output in `/home/user/success.log` contains the successful JSON response from the gRPC mock server.