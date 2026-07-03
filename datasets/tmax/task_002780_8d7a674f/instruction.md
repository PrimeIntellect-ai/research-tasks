You are a platform engineer maintaining a CI/CD pipeline for a new secure compute platform. A pipeline test for the platform's WebSocket-based stack machine emulator is failing. 

There are three issues you need to resolve in the `/home/user/ci_env` directory:

1. **Reverse Proxy Configuration**: The CI environment uses an Nginx reverse proxy to route traffic to the emulator, but the proxy is dropping WebSocket connections. The Nginx configuration file is at `/home/user/ci_env/nginx.conf`. It listens on port 8080 and proxies to port 9000. Fix the configuration so that it correctly forwards WebSocket connection upgrades. Nginx can be started with `nginx -c /home/user/ci_env/nginx.conf`.

2. **Emulator Implementation**: The backend emulator is located at `/home/user/ci_env/emulator.py`. It runs a WebSocket server on port 9000. The message parsing is in place, but the core stack machine interpreter logic is missing inside the `process_command` function. 
Implement a simple stack machine that processes a string of space-separated tokens. Support the following operations:
   - `PUSH <int>`: Pushes an integer onto the stack.
   - `ADD`: Pops the top two elements, adds them, and pushes the result.
   - `MUL`: Pops the top two elements, multiplies them, and pushes the result.
The function should return the final integer value at the top of the stack as a string. For example, `PUSH 2 PUSH 3 ADD PUSH 4 MUL` should return `"20"`. If the stack is invalid or empty at the end, return `"ERROR"`.

3. **Performance Benchmarking**: The CI pipeline requires a benchmark script to measure emulator throughput. Create a Python script at `/home/user/ci_env/benchmark.py` that connects to the emulator through the Nginx reverse proxy (`ws://127.0.0.1:8080`). 
The script must:
   - Send exactly 100 WebSocket messages containing the payload: `PUSH 5 PUSH 10 ADD PUSH 2 MUL`
   - Wait for the response for each message and verify it equals `"30"`.
   - Measure the total time taken to complete all 100 requests.
   - Write the results to `/home/user/ci_env/benchmark_report.json` in the exact following format:
     `{"successful_requests": 100, "total_time_ms": <total_time_in_milliseconds>}`

Make sure to start the emulator and Nginx in the background before running your benchmark script. The `websockets` Python library is available.