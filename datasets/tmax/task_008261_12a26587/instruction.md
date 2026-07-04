You are a DevSecOps engineer tasked with enforcing policy as code and auditing a vulnerable authentication service.

Your task consists of the following phases:

1. **Reverse Engineering & Decryption**: 
   You have been provided with a compiled legacy binary at `/home/user/legacy_verifier` and an encrypted policy file at `/home/user/policy.enc`. 
   - Analyze the `legacy_verifier` binary to extract a hardcoded AES-256-CBC encryption key (32 bytes) and IV (16 bytes).
   - Use these credentials to decrypt `/home/user/policy.enc` into a plaintext file at `/home/user/policy.txt`.

2. **Code Auditing & Vulnerability Fix**:
   The directory `/home/user/auth_server` contains a Rust project. The function `get_redirect_url(input: &str) -> String` in `/home/user/auth_server/src/main.rs` contains a vulnerability commonly found in login flows that allows attackers to redirect users to malicious external domains.
   - Identify the standard CWE ID for this vulnerability.
   - Fix the vulnerability in `get_redirect_url`. The new logic must ensure that if the provided `input` is a valid relative path (it MUST start with a single `/` and MUST NOT start with `//`), it returns the `input` as a `String`. Otherwise, it should securely default to returning `"/dashboard"`.
   - Compile the fixed project using `cargo build`.

3. **Reporting**:
   Generate a JSON report at `/home/user/report.json` with the following exact keys:
   - `"cwe_id"`: The CWE ID of the vulnerability you identified (format: `"CWE-XXX"`).
   - `"decrypted_policy"`: The exact plaintext string extracted from the decrypted policy file.
   - `"fixed_binary_sha256"`: The SHA-256 hash of the compiled debug binary located at `/home/user/auth_server/target/debug/auth_server`.

Ensure all code compiles successfully and the JSON report is valid.