You are a compliance analyst tasked with ensuring our internal token validation and audit logging system works exactly as specified by our legacy compliance oracle. 

We have a vendored third-party C++ package located at `/app/libauthtoken-1.2.0` which is responsible for token generation and validation. Unfortunately, this specific version has a deliberate perturbation: the `Makefile` has an incorrect compiler flag that prevents it from linking properly with OpenSSL, and the `src/validator.cpp` file is missing a critical boundary check for the token expiry field, causing it to fail strict compliance checks.

Your tasks are as follows:

1. **Fix the Vendored Package:**
   Navigate to `/app/libauthtoken-1.2.0`. Fix the `Makefile` (ensure it links `-lcrypto`) and patch `src/validator.cpp` so that it rejects any token where the `exp` (expiration) claim is missing or mathematically overflows (assume maximum valid Unix timestamp is `2147483647`). Build the package to produce the `token_tool` binary.

2. **Create the Audit Wrapper:**
   Write a bash script at `/home/user/audit_wrapper.sh` that takes exactly one argument: a raw base64-encoded token string.
   This script must use the compiled `/app/libauthtoken-1.2.0/token_tool validate <token>` to verify the token.
   Based on the output of `token_tool`, your bash script must enforce Content Security Policy (CSP) headers and pattern match for intrusion detection (e.g., if the token's subject contains `<script>` or `UNION SELECT`, it must be flagged).
   
   Your script must output exactly one line to standard output in the following format:
   `AUDIT_LOG: status=[VALID|INVALID|MALICIOUS] subject=[sub] timestamp=[current_unix_ts]`
   
   If the token contains malicious SQLi/XSS payloads in the subject, status must be `MALICIOUS`. If `token_tool` rejects it, status must be `INVALID`. Otherwise, `VALID`.

You must ensure your `/home/user/audit_wrapper.sh` behaves *bit-exact equivalent* to our legacy system. We will test your script against thousands of generated tokens to ensure the output matches our reference oracle perfectly.

Ensure your script is executable.