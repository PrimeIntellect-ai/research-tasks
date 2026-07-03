You are a script developer tasked with creating a robust testing utility for our new high-performance URL routing and parameter parsing engine. The engine is currently compiled as a stripped binary located at `/app/router_engine_stripped`. 

We suspect the binary suffers from memory safety issues (like buffer overflows or undefined behavior) when handling edge-case URL parameters and malformed route paths. 

Your objectives are:
1. **Property-Based Fuzzer**: Write a Python script at `/home/user/fuzz_router.py` that uses the `hypothesis` library (you may need to install it) to generate diverse, edge-case URL strings. The script should invoke the binary using `subprocess` (`/app/router_engine_stripped <generated_url>`) and monitor its exit codes to detect crashes (e.g., segmentation faults).
2. **Crash Logging**: Whenever a crash is detected, log the exact URL that caused the crash to `/home/user/crashes.log`. Each line in this file must contain exactly one crashing URL. Your script should run until it finds several distinct crashing inputs or completes its test suite.
3. **CI/CD Pipeline Setup**: Create a generic GitHub Actions workflow file at `/home/user/.github/workflows/fuzz.yml` that sets up Python, installs dependencies, and runs your `fuzz_router.py` script.

The binary accepts a single argument (the URL path, starting with `/`) and prints parsed parameters to stdout. 
Example usage: `/app/router_engine_stripped "/api/v1/users?id=123&sort=desc"`

Ensure your fuzzer is efficient and explores edge cases like overly long parameter values, weird Unicode characters, and missing keys.