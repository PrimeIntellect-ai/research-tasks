As a security auditor, you need to fix a critical vulnerability in a web application's file upload component. The current Rust-based path sanitization service is susceptible to path traversal and filename-based injection attacks, allowing attackers to upload files outside the intended directories or inject malicious payloads via file names.

We have a vendored Rust package located at `/app/path_sanitizer-1.0.0/`. It is meant to be a CLI tool that takes a base directory and a user-provided filename/path, and outputs the fully resolved, safe absolute path. If the path violates security rules, it must output specific error codes.

However, the vendored package has been deliberately perturbed:
1. It fails to build because its build configuration (`Cargo.toml`) is broken/incomplete.
2. The code in `src/main.rs` has logical flaws causing the path traversal.

I have provided a perfectly secure, reference implementation (a stripped binary) at `/app/oracle_sanitizer`.

Your task:
1. Reverse engineer and test `/app/oracle_sanitizer` by passing it various inputs to understand its exact behavior, security rules, and error messages. It accepts arguments like this: `/app/oracle_sanitizer <base_directory> <untrusted_input>`.
2. Analyze the rules it applies for:
   - Null bytes (e.g. `\0` or `%00`)
   - Path traversal attempts (e.g. `../`, `..%2f`)
   - XSS injection in filenames (e.g. `<script>`, `>`)
   - Ensuring the final canonical path strictly resides within the `<base_directory>`.
3. Fix the `Cargo.toml` in `/app/path_sanitizer-1.0.0/` so the project can be built.
4. Rewrite or fix `src/main.rs` so that its output is **bit-exact equivalent** to the oracle for all possible inputs.
5. Build your fixed package. Your final executable must be located at `/app/path_sanitizer-1.0.0/target/debug/path_sanitizer`.

Note: An automated fuzzer will run thousands of mutated payloads against both `/app/oracle_sanitizer` and your built binary to ensure identical standard output and standard error for every edge case.