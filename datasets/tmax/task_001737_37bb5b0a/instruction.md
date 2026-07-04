You are a mobile build engineer responsible for maintaining the backend pipelines that process build artifacts and telemetry from mobile clients. 

We are migrating our telemetry API gateway from an old, slow C++ binary to a new, high-performance Rust implementation. However, the junior engineer who started the Rust port struggled with Rust's ownership and borrow checker rules, and the code currently does not compile. Additionally, the request validation and data decoding logic is incomplete.

Your tasks are as follows:

1. **Fix the Rust Implementation:**
   Navigate to `/home/user/telemetry_gate`. You will find a Rust project with compilation errors in `src/main.rs`. Fix the borrow checker, lifetime, and ownership errors without changing the overall architectural flow.

2. **Implement Character & Data Decoding:**
   The incoming telemetry files are JSON objects containing a `payload` string. This string is doubly encoded: first Base64 encoded, and then URL encoded. 
   You must update the Rust code to properly decode the payload (URL decode -> Base64 decode) and then validate it.

3. **Reverse-Engineer the Validation Logic:**
   We do not have the original documentation for what constitutes a "malicious" payload. However, we have the original stripped C++ binary at `/app/legacy_gate`. 
   You can treat `/app/legacy_gate <file_path>` as a black-box oracle. It exits `0` for valid telemetry and `1` for malicious telemetry. Use it to determine the exact string patterns or anomalies that cause a payload to be rejected, and replicate this exact logic in your Rust program.

4. **Pass the Adversarial Corpora:**
   Your compiled Rust binary (`/home/user/telemetry_gate/target/release/telemetry_gate`) must perfectly filter the provided corpora:
   - Accept (exit 0) 100% of the files in `/home/user/corpora/clean/`
   - Reject (exit 1) 100% of the files in `/home/user/corpora/evil/`

5. **Performance Benchmarking:**
   Once your Rust binary successfully compiles and correctly passes the corpora, build it in release mode (`cargo build --release`). 
   Then, run the provided benchmarking script: `bash /home/user/run_benchmark.sh`. 
   Save the exact standard output of this script into a file at `/home/user/benchmark_results.txt`.

Ensure your final binary is located at `/home/user/telemetry_gate/target/release/telemetry_gate` and takes a single file path as its command-line argument.