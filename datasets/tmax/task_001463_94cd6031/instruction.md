You are an open-source maintainer reviewing a failing pull request for `PolyBenchWS`, a polyglot WebSocket benchmarking suite. The project consists of a C++ WebSocket server, a Rust-based load generator, and a suite of Bash utilities for CI/CD payload generation.

The PR author attempted to implement a high-performance, purely Bash-based payload normalizer (`/home/user/ws_normalizer.sh`) to prepare test messages before they are broadcasted via WebSockets. However, the CI integration tests are failing, the polyglot build orchestration is broken, and the normalizer produces incorrect output.

Your task is to fix the PR by completing the following steps:

1. **Information Extraction (Image)**:
   The strict protocol requirements are defined in an image artifact left by the original architect at `/app/protocol_spec.png`. You must use OCR (e.g., `tesseract`) to read this image. It contains a secret `MAGIC_HEADER` string required for all WebSocket payloads.

2. **Fix the Payload Normalizer (Bash)**:
   Create or fix the bash script at `/home/user/ws_normalizer.sh`. The script must take exactly one argument (the raw payload string) and output the normalized string to `stdout`.
   The normalization rules are:
   - Prepend the magic header extracted from the image, followed by a colon and a single space (e.g., `HEADER_VALUE: `).
   - Convert the entire *original* payload string to uppercase.
   - Replace all space characters (` `) in the *original* payload string with underscores (`_`).
   - Example: If the header is `XYZ!` and the input is `hello world`, the output must be `XYZ!: HELLO_WORLD`.
   - The script must be executable (`chmod +x`).

3. **Polyglot Build & Benchmark (Contextual)**:
   While your primary deliverable is the Bash script, in a real scenario you would build the C++ server and Rust client in `/home/user/repo` to run the integration tests and performance benchmarks over WebSockets. (Note: For this automated verification, ensuring the Bash script is bit-exact with the expected protocol is sufficient).

Ensure your script at `/home/user/ws_normalizer.sh` is robust, fast, and handles arbitrary alphanumeric input strings with spaces. The automated test will fuzz your script against a reference binary to ensure it correctly normalizes thousands of random payloads.