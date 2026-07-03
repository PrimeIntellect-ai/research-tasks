You are a QA engineer responsible for setting up a high-performance benchmarking gateway for our multi-service test environments. The gateway is written in C and uses a custom state-machine based parser to process test routing URLs, record benchmarking state in Redis, and forward requests to our gRPC test backends. 

Currently, the project in `/home/user/app` fails to function correctly due to two main issues:
1. **Memory / Pointer Issues:** The C-based URL parser (`/home/user/app/src/parser.c`) mimics a Rust-like strict ownership model but currently has severe memory corruption, double-free, and dangling pointer bugs when parsing the custom scheme (`test-env://[service]/[method]?bench=[ms]&retry=[count]`). It crashes on complex inputs.
2. **Environment Configuration:** The multi-service test environment is not wired up correctly. 

**Your Tasks:**

**Part 1: Fix the State Machine Parser**
1. Inspect and fix the memory management and pointer logic in `/home/user/app/src/parser.c`. The parser must correctly extract the service name, method name, bench time, and retry count, and format them into a strict JSON string.
2. Build the standalone parser CLI. We use a Makefile. Run `make parser` to produce `/home/user/app/build/url_parser`.
3. The output of your fixed `/home/user/app/build/url_parser` (which reads a URL from `stdin` and writes JSON to `stdout`) MUST be bit-exact equivalent to our stripped reference oracle located at `/home/user/oracle/url_parser_oracle` for any valid or invalid input string.

**Part 2: Multi-Service Composition & Integration**
We have three components in our test environment:
- A Redis instance for rate limiting and state tracking.
- A Python-based gRPC mock backend located in `/home/user/app/backend/`.
- The C benchmark gateway `/home/user/app/build/gateway` (build with `make gateway`).

1. Start the Redis server locally on its default port (6379).
2. Start the Python mock backend by running `python3 /home/user/app/backend/mock_grpc_server.py`. It listens on port 50051.
3. Edit the gateway configuration file at `/home/user/app/config/gateway.json` to correctly point to the Redis port (`6379`) and the backend gRPC port (`50051`).
4. Start the gateway service. It will listen on port 8080.

To verify your setup is complete, you should be able to run:
`curl -d "test-env://auth/login?bench=50&retry=3" http://localhost:8080/benchmark`
and receive a successful JSON benchmarking report. Leave the gateway, Redis, and python services running in the background when you are finished.