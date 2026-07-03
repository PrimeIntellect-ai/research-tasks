You are a DevOps engineer investigating a failed log ingestion pipeline. 

The system comprises three components located in `/app`:
1. `redis`: A local Redis server.
2. `log_generator.py`: A Python script simulating an upstream service that streams log lines over TCP on port 9000.
3. `log_parser`: A Rust application (in `/app/log_parser/`) intended to listen on port 9000, parse the raw logs, extract a timestamp and a precision metric, and push the JSON-formatted result to Redis on port 6379.

Currently, the pipeline is completely broken:
- The `log_parser` Rust project fails to compile due to a build error.
- Even if fixed, forensics from previous crashes indicate that the parser gets stuck in an infinite loop when encountering log lines with malformed tag blocks (e.g., missing closing brackets).
- Furthermore, we noticed precision loss in our forensics dashboard. The metric values in the logs (high-precision floating point numbers) are losing their trailing decimals when parsed and serialized by the Rust app.

Your task:
1. Fix the build errors in `/app/log_parser/`.
2. Debug and fix the infinite loop/recursion issue in `src/main.rs` that occurs when parsing tags.
3. Fix the precision loss issue so the parsed metric retains its exact `f64` representation.
4. Compile the fixed binary (using `cargo build --release`). 
5. Start the Redis service and the log parser.
6. Execute `/app/log_generator.py` to send the test log payload.

The compiled Rust binary at `/app/log_parser/target/release/log_parser` must behave EXACTLY like the reference oracle binary. When run in standalone mode (e.g., passing a log line via stdin, which is how it processes individual lines internally), it must output the exact same JSON string as the oracle.

Please apply the fixes, bring up the services, and ensure the data successfully flows into Redis.