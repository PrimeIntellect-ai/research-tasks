You need to fix and optimize a polyglot microservice architecture located in `/home/user/app`. The system consists of three services:
1. A Redis cache.
2. A Rust-based WebSocket math engine (handles fast Fourier transforms and matrix operations).
3. A Python FastAPI gateway that routes HTTP REST requests to the Rust WebSocket engine.

Currently, the system is broken in several ways:
1. **Compilation Failure:** The Rust project in `/home/user/app/rust_engine` fails to compile. A core mathematical function (`calculate_determinant`) is missing. We have a reference implementation in Python located at `/home/user/app/reference_math.py`. You need to translate this Python function into Rust and place it in the appropriate module to fix the build.
2. **Routing and WebSockets:** The Python gateway in `/home/user/app/python_gateway/main.py` has broken URL routing and fails to establish a WebSocket connection to the Rust engine. Fix the FastAPI routes so that `POST /api/v1/matrix/determinant` correctly parses the JSON payload, opens a WebSocket to `ws://localhost:8001/math`, sends the payload, awaits the result, and caches it in Redis before returning the HTTP response.
3. **Build Orchestration:** Write a script `/home/user/app/build_and_start.sh` that compiles the Rust project (in release mode), starts Redis, starts the Rust WebSocket server on port 8001, and starts the Python gateway on port 8000 using Uvicorn.

**Performance Requirement:**
We are measuring the system's performance. The final architecture must achieve a 95th percentile latency (p95) of less than 25 milliseconds when hit with a burst of 1000 requests. 

Please fix the code, write the startup script, and ensure all services are running and correctly communicating. Leave the services running in the background when you are done.