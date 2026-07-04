You are a QA engineer responsible for setting up and debugging the end-to-end test environment for our new high-throughput Telemetry Ingestion Pipeline.

The system consists of three main components:
1. **Redis**: Used for rate-limiting and data storage (standard local instance on port 6379).
2. **Python Backend**: A Flask REST API located in `/app/backend/` running on port 5000. It receives validated telemetry data and stores it in Redis.
3. **Rust WebSocket Proxy**: A Rust-based WebSocket server located in `/app/rust-proxy/` running on port 8080. It acts as the front-line ingestor, receiving JSON frames over WebSockets, validating them, and forwarding the valid ones to the Python backend via HTTP POST.

Unfortunately, the test environment is currently broken:
- The Rust proxy fails to compile due to several lifetime and borrow-checker issues in `src/parser.rs`.
- The Rust proxy is missing the custom checksum and error-correcting validation logic. The reference implementation for this logic is provided in Python at `/app/reference/checksum.py`. You must translate this logic into Rust and integrate it into the proxy's validation pipeline.

Your objectives:
1. **Fix the Rust Compilation:** Resolve the lifetime errors in `/app/rust-proxy/src/parser.rs` without changing the external structs' data semantics.
2. **Implement Checksum Validation:** Translate the logic from `/app/reference/checksum.py` into the Rust proxy. The proxy must drop any WebSocket frame that fails this checksum validation or is structurally malformed.
3. **Bring Up the Environment:** Configure and start Redis, the Python Backend, and the compiled Rust Proxy.
4. **Adversarial Testing:** We have two corpora of telemetry payloads:
   - `/app/corpora/clean/`: Contains valid, well-formed JSON payloads with correct checksums.
   - `/app/corpora/evil/`: Contains malformed structures, invalid checksums, and rate-limit abusive payloads.
   The Rust proxy MUST accept and forward 100% of the clean payloads to the backend, and MUST reject (drop and not forward) 100% of the evil payloads.

When you have fixed the code, successfully started all three services, and are ready for the automated test suite to run, create a file named `/home/user/environment_ready.log` containing the text `READY`. The verifier will then establish WebSocket connections to `ws://localhost:8080` to inject the corpora and check the database state.