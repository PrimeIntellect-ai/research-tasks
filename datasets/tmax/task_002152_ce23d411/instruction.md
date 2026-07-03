You are acting as a security engineer and penetration tester. We have obtained a batch of server logs and process command-line captures. We suspect that some of these logs contain leaked credentials (e.g., passwords passed as command-line arguments) and malicious XSS payloads attempting to exploit our internal log viewer.

Your task is to write a Rust CLI application that classifies these log files as either malicious/leaky or clean.

1. **Vendored Package Fix:**
   We rely on a local vendored Rust crate called `log-parser` located at `/app/vendored/log-parser-1.0.0`. However, the previous developer made a mistake in its configuration, and it currently fails to compile. You must identify and fix the perturbation in `/app/vendored/log-parser-1.0.0` so that it builds successfully.

2. **Detector Implementation:**
   Create a new Rust binary project at `/home/user/detector`.
   Your tool must take a single command-line argument: the path to a log file.
   It must use the fixed `log-parser` crate as a local dependency to parse the file. The `log-parser` crate exposes a function `pub fn parse_log(input: &str) -> Vec<String>` which extracts relevant tokens (arguments and URL parameters) from the raw log text.

3. **Classification Logic:**
   Iterate over the tokens extracted by `log-parser`. Flag the file as "evil" if ANY token contains:
   - A credential leak: Any string matching the exact format `password=<value>` or `--password=<value>` where `<value>` is at least 1 character long.
   - An XSS payload: Any token containing the case-insensitive substrings `<script>`, `javascript:`, or `onerror=`.
   
   If the file is "evil", your program must exit with status code `1`.
   If the file is "clean" (none of the above are found), your program must exit with status code `0`.

We have provided two directories of test files for you to evaluate your tool:
- `/app/data/evil/` (All files here MUST cause your tool to exit with code `1`)
- `/app/data/clean/` (All files here MUST cause your tool to exit with code `0`)

Build your final compiled binary at `/home/user/detector/target/release/detector`.