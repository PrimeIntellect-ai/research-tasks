You are a build engineer responsible for setting up a new CI/CD performance benchmarking pipeline for a Rust-based parser. 

We have a Rust project located at `/home/user/rust_parser`. It contains a state machine parser that processes log files. We need to create a bash script that compiles this parser, benchmarks its execution, and serializes the performance metrics into a JSON artifact.

Your task is to write a bash script at `/home/user/ci_benchmark.sh` that performs the following steps exactly:
1. Navigate to `/home/user/rust_parser`.
2. Build the Rust project in release mode.
3. Run the compiled binary (`target/release/rust_parser`) on the input file `/home/user/rust_parser/input.log`. You must measure its performance using `/usr/bin/time -v`.
4. Parse the `time -v` stderr output to extract exactly two values:
   - `User time (seconds)`
   - `Maximum resident set size (kbytes)`
5. Serialize these values into a valid JSON file saved to `/home/user/artifacts/bench_results.json`. The JSON file must have exactly this format:
   `{"user_time_seconds": <float>, "max_rss_kb": <integer>}`

Make sure the script is executable (`chmod +x /home/user/ci_benchmark.sh`). 

Note: You can assume `/home/user/rust_parser` and `/home/user/artifacts` directories already exist, and the input log is present. Use standard shell utilities (`grep`, `awk`, `sed`, etc.) to parse the output.