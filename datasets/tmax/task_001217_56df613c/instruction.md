You are an operations engineer triaging severe incidents in our telemetry ingestion pipeline. 

We have a legacy binary `/app/telemetry_oracle` that correctly parses our proprietary binary telemetry protocol. Unfortunately, the original source code is lost, and the binary is stripped and difficult to modify. 

Our team attempted to rewrite the parser in Rust to improve maintainability and performance. The project is located at `/home/user/telemetry_parser`. However, the Rust replacement is failing in production:
1. It intermittently crashes when processing corrupted packet payloads.
2. It occasionally hangs indefinitely (infinite loop/deep recursion) and consumes 100% CPU on certain malformed packet sequences.

Your task is to debug and fix the Rust implementation in `/home/user/telemetry_parser` so that it:
1. Gracefully handles corrupted input without panicking (e.g., skips the corrupted packet or recovers).
2. Fixes the loop termination and recursion bugs that cause hangs.
3. Produces JSON output that matches the behavior of `/app/telemetry_oracle`.

To test your implementation, we have provided a dump of network traffic at `/home/user/data/packets.bin`. 
You can run the legacy oracle to see the expected output: `/app/telemetry_oracle /home/user/data/packets.bin > reference.json`.

**Requirements:**
- Fix the code in `/home/user/telemetry_parser/src/main.rs`.
- Ensure `cargo build --release` successfully compiles your fixed code.
- Ensure your compiled binary can process `/home/user/data/packets.bin` and output the results to `/home/user/parsed_telemetry.json` without crashing or hanging.
- The output format must be one JSON object per line, matching the oracle's output keys and values for all valid packets.

A post-run automated test will compile your code and test it against a held-out dataset of heavily corrupted packets to calculate your parse accuracy metric.