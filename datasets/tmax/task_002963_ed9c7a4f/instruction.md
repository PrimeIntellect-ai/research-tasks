You are an incident responder investigating a data processing node. We have a vendored package, `secure_etl_tool-1.0`, located at `/app/vendor/secure_etl_tool-1.0/`. It parses sensitive encrypted logs.

Recently, security auditing revealed two critical issues:
1. The tool's build is broken. Its C-extension for file integrity verification fails to compile because of a deliberate misconfiguration in its `Makefile`, causing the tool to fall back to a terribly slow, insecure pure-Python stub.
2. We suspect the tool leaks TLS/SSL decryption keys to `/proc`. When the Python application spawns a subprocess to decrypt incoming logs, it appears to pass the key password as a command-line argument, which is visible to any local user monitoring process arguments.

Your objectives:
1. **Fix the Build Environment**: Inspect the `Makefile` inside `/app/vendor/secure_etl_tool-1.0/`. Identify and correct the include path or environment variable perturbation so the C-extension (`fast_integrity.c`) compiles successfully. Compile it using `make`.
2. **Auditing and Patching**: Use reverse engineering principles or standard auditing bash tools to find where the Python code (`worker.py`) spawns subprocesses (likely `openssl` or similar). Patch `worker.py` so that it passes the TLS decryption password securely (e.g., via environment variables or stdin) instead of a command-line argument.
3. **Verify Integrity and Certificates**: Ensure the tool correctly loads the TLS certificate from `/app/certs/client.pem`. The fallback Python code bypassed certificate validation entirely; your compiled C-extension will enforce it. Ensure the proper paths are set in `config.json`.
4. **Pass the Metric Benchmark**: The tool must be both secure and performant. Run the evaluation suite by executing `/home/user/run_benchmark.sh`. This script will launch your patched tool against 5,000 log entries while concurrently monitoring `/proc` for leaked passwords.
   
The benchmark will output a metric score to `/home/user/benchmark_result.txt` representing logs processed per second. If any credentials are leaked to `/proc` during the run, the score defaults to `0.0`. 

You must successfully patch the application and achieve a benchmark score of at least `250.0` (logs per second) with zero leaks. Do not modify `/home/user/run_benchmark.sh`.