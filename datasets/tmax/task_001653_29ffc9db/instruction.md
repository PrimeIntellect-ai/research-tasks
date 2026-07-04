You are tasked with porting an esoteric language emulator (a Brainfuck interpreter) to work as a minimal containerized web API using C++. The original build configuration is broken, the web routing logic is incomplete, and we need a basic CI pipeline to ensure it builds correctly.

The project is located in `/home/user/emulator_port`. It contains:
1. `bf_interpreter.hpp`: A working Brainfuck interpreter.
2. `server.cpp`: A raw TCP socket server that listens on port 8080. It currently accepts connections but does not parse HTTP requests, route them, or validate input.
3. `CMakeLists.txt`: A broken CMake build file that fails to compile the C++17 code and lacks thread support.
4. `benchmark.py`: A Python script to benchmark the API performance.

Your objectives:

1. **Fix the Build System:**
   Fix the `CMakeLists.txt` in `/home/user/emulator_port` so that it successfully compiles `server.cpp`. It needs to enforce C++17 standard and properly link the system threading library (`pthread` via CMake's `Threads` package).

2. **Implement API Routing and Validation:**
   Modify `server.cpp` to correctly handle incoming HTTP `GET` requests.
   - Parse the request to extract the `code` parameter from the path: `/execute?code=<bf_code>`. (Assume the code is passed raw, no URL encoding for this minimal setup).
   - **Validation & Rate Limiting (Security):** Before execution, validate the `code` string. If it contains *any* characters other than `+`, `-`, `<`, `>`, `[`, `]`, `.`, `,` (the 8 standard BF instructions), you must respond with:
     `HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid characters`
   - If the code is valid, execute it using the provided `execute_bf(code)` function.
   - Return the output with a successful HTTP response:
     `HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n<interpreter_output>`
   - Ensure you correctly close the socket after responding (Connection: close behavior).

3. **Setup CI/CD Pipeline:**
   Create a GitHub Actions workflow file at `/home/user/emulator_port/.github/workflows/ci.yml`. It should define a single job that:
   - Uses an `ubuntu-latest` runner.
   - Configures CMake, builds the target `bf_server`.
   - The workflow file format must be syntactically valid YAML.

4. **Benchmark & Log:**
   Build your server, run it in the background, and execute the benchmark:
   `python3 /home/user/emulator_port/benchmark.py > /home/user/emulator_port/benchmark_metrics.log`
   
Ensure your server process is gracefully terminated after the benchmark completes. Leave the `benchmark_metrics.log` and `.github/workflows/ci.yml` in place for automated verification.