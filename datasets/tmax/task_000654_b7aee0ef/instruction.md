You are acting as a performance engineer debugging our new high-performance log analytics pipeline. We have a multi-component system located in `/home/user/log_pipeline` that parses JSON log files, performs floating-point latency aggregations, and queries a local in-memory store. Unfortunately, the system is in a broken state, and we need you to fix it and build a protective sanitiser.

Here is what you need to do:

1. **Fix the Build and Environment:** 
   The Rust project in `/home/user/log_pipeline` currently fails to build. Diagnose the compilation and environment errors. There is an environment misconfiguration related to system dependencies, as well as a compilation error in `src/query.rs` causing incorrect query results. Fix the build so `cargo build --release` succeeds.

2. **Fix the Analytics and Parsing Bugs:**
   - The parser in `src/parser.rs` panics on certain format edge-cases (specifically, unescaped control characters in the "user_agent" field). Repair it to gracefully skip these malformed fields rather than crashing.
   - The latency aggregation in `src/analytics.rs` calculates a rolling variance but suffers from floating-point precision issues (catastrophic cancellation). We have provided a stripped black-box binary oracle at `/app/analytics_oracle`. Your Rust module's variance output must exactly match the output of `/app/analytics_oracle < input.txt` up to 5 decimal places.

3. **Diagnose and Fix the Concurrency Leak:**
   When running the pipeline under load with cancellations, it leaks Tokio tasks. Identify the race condition or missing cancellation handler in `src/worker.rs` and fix it so memory remains stable.

4. **Build an Adversarial Sanitiser:**
   The parser is still vulnerable to crafted "log bombs" (deeply nested JSON objects and extremely long keys) that degrade performance. Create a standalone Rust CLI tool at `/home/user/sanitiser` (initialize it with `cargo new`) that acts as a pre-filter. 
   - It must take two arguments: an input directory of log files and an output directory (`cargo run -- <input_dir> <output_dir>`).
   - It must parse each log line, determine if it is malicious, and write only the benign log lines to files with the same names in the output directory.
   - Malicious logs contain keys longer than 64 characters or have a nesting depth strictly greater than 4.

Please complete these steps. We will test your sanitiser against our internal corpora of clean and evil logs. We will also run our integration tests against `/home/user/log_pipeline`.