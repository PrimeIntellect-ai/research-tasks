We are experiencing severe instability in our IoT telemetry platform. Legacy devices occasionally send corrupted or truncated binary payloads, and a recent update has caused the Rust ingestion service to completely crash (panic) when handling these edge cases. 

Our system consists of three components:
1. **Redis**: Used for intermediate telemetry caching (port 6379).
2. **Telemetry Ingester (Rust)**: Located in `/app/telemetry_ingester`. It listens on TCP port `8080`, parses a custom length-prefixed binary protocol, and pushes valid records to Redis.
3. **Telemetry API (Python)**: Located in `/app/api`. It listens on HTTP port `9090` and exposes the aggregated metrics from Redis.

**The Regression:**
The platform was perfectly stable at git tag `v1.0.0` in the `/app/telemetry_ingester` repository. Since then, over 200 commits have been merged to the `main` branch. One of these commits introduced a high-performance "zero-copy" parser that unfortunately panics due to an out-of-bounds slice access when a payload's declared length exceeds the actually transmitted bytes. 

**Your objectives:**
1. **Bisect the regression:** Use `git bisect` in `/app/telemetry_ingester` between `v1.0.0` (good) and `HEAD` (bad) to find the exact commit hash that introduced the panic. 
2. Write the 40-character commit hash of the first bad commit to `/home/user/bisection_result.txt`.
3. **Fix the bug:** At `HEAD` (the `main` branch), repair the `src/parser.rs` file so that if a declared length exceeds the buffer, the parser returns a `ParseError::Truncated` instead of panicking.
4. **Deploy the stack:** 
   - Compile your fixed Rust service (`cargo build --release`).
   - Start the Redis server (a local installation is available; use default configuration on port 6379).
   - Start the Python API (`python3 /app/api/main.py`).
   - Start your fixed Rust ingester (`/app/telemetry_ingester/target/release/telemetry_ingester`).
   
Leave all three services running in the background. Our automated verifier will connect to both the TCP ingestion port (8080) and the HTTP API port (9090) to validate the fix and system functionality.