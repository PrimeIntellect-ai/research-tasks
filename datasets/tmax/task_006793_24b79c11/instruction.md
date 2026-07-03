You are tasked with modernizing a legacy system. We have a simple stack machine emulator written in Python 2. We need to port it to Python 3, wrap it in a REST API, put a reverse proxy in front of it, and design a gRPC schema for future migration. 

Here are the specific requirements:

1. **Migrate the Emulator**: 
   Look at `/home/user/legacy_emulator.py`. It is a Python 2 script containing a function `evaluate(program_string)` that evaluates postfix expressions (like "2 3 ADD"). Create a new Python 3 file at `/home/user/server.py` that includes this logic (ported to Python 3).

2. **REST API Construction**:
   In `/home/user/server.py`, implement a Python 3 HTTP server (using the built-in `http.server` module or a lightweight framework like `Flask` if you install it locally) that listens on `127.0.0.1:9090`. 
   It must expose a single POST endpoint `/execute`. It should accept JSON in the format `{"program": "<string>"}` and return JSON in the format `{"result": <integer>}`.
   Start this server in the background.

3. **Reverse Proxy Configuration**:
   Create an Nginx configuration file at `/home/user/nginx.conf`. It should run as a non-root user (configure `pid` and all `_temp_path` directives to use `/tmp/` so it doesn't require sudo).
   Configure a server listening on `127.0.0.1:8080` that reverse-proxies all requests for `/execute` to your Python 3 REST API at `127.0.0.1:9090`.
   Start Nginx in the background using this config (`nginx -c /home/user/nginx.conf`).

4. **gRPC / Protobuf Design**:
   We plan to eventually move from REST to gRPC. Design the Protocol Buffers schema for this emulator.
   Create `/home/user/emulator.proto`.
   - It must use `syntax = "proto3";`
   - Define a package named `emulator`.
   - Define a service `EmulatorService` with an RPC method `ExecuteProgram` that takes a `ProgramRequest` and returns a `ProgramResponse`.
   - `ProgramRequest` should have a single string field `program` (field number 1).
   - `ProgramResponse` should have a single int32 field `result` (field number 1).

5. **Testing and Verification (Bash)**:
   Write a Bash script at `/home/user/test_system.sh`. When executed, this script should use `curl` to send a POST request to your Nginx reverse proxy at `http://127.0.0.1:8080/execute` with the payload `{"program": "5 10 MUL 2 ADD"}`.
   The script must save the exact HTTP response body (the JSON output) to `/home/user/migration_result.log`.
   Make sure the script is executable and run it once so the log file is generated.