You are a compliance analyst handling web application security audit trails. We are migrating our legacy log sanitizer to Rust to improve process isolation and memory safety, but we are working in an air-gapped environment with a pre-vendored dependencies folder. 

Your objective is to fix a broken vendored dependency and implement a Rust log sanitizer that exactly mimics the behavior of our proprietary oracle binary.

### Step 1: Fix the Vendored Package
The `regex` crate (version 1.10.4) has been vendored at `/app/vendor/regex-1.10.4`. However, a previous developer accidentally broke its `Cargo.toml` by changing the package name to `name = "regex-broken"`. 
Fix the `Cargo.toml` in the vendored package so it can be correctly used as `regex` by your project.

### Step 2: Implement the Audit Sanitizer
Create a new Rust binary project at `/home/user/audit_tool`. You must use the fixed vendored `regex` crate (by specifying the local path in your `Cargo.toml`).

Your Rust program must read raw audit log lines from standard input (one per line) and print the processed lines to standard output. 

You must implement the following sanitization rules (combining CWE identification and password redaction) exactly as the legacy system did:
1. **CWE Identification:** If the input line contains the exact substring `CWE-79` or `CWE-89`, prepend the string `[ALERT] ` to the beginning of the line.
2. **Password/PIN Redaction:** Use the `regex` crate to find any occurrences of the literal `pin=` followed immediately by one or more digits (`\d+`). Replace only the digits with `XXXX`. For example, `pin=1234` becomes `pin=XXXX`.
3. If a line meets both criteria, prepend the alert *and* redact the PIN. 
4. Output the exact modified string with a trailing newline.

### Step 3: Verification
Your compiled binary must be placed at `/home/user/audit_tool/target/release/sanitizer` (compile it using `cargo build --release`).
Our automated testing framework will run a strict fuzzing equivalence test against our legacy binary located at `/app/oracle/audit_sanitizer`. Your program must produce bit-exact identical standard output for any given string input.

Write the code, fix the crate, and ensure your binary is compiled and ready at the specified path.