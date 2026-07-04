You are a DevSecOps engineer tasked with enforcing "policy as code" for a legacy authentication module. The module processes JSON Web Tokens (JWTs), relies on an embedded issuer ID, and uses a local certificate chain. Recent security audits suggest the system might be vulnerable to JWT signature bypass attacks (e.g., `alg=none`) and may have misconfigured certificates.

Your objective is to write a Python script at `/home/user/enforce_policy.py` that audits these components and generates a security report. 

Your script must perform the following tasks:

1. **Binary Analysis**: Analyze the ELF executable located at `/home/user/legacy_auth_bin`. Extract the embedded Issuer ID. The ID is stored as a hardcoded string in the read-only data section (`.rodata`) in the format `ISSUER_ID=<random_string>`.

2. **Certificate Chain Validation**: Validate the certificate chain located in `/home/user/certs/`. The directory contains `ca.pem`, `intermediate.pem`, and `leaf.pem`. You must determine if `leaf.pem` is cryptographically valid and chains up to the trusted root `ca.pem` through `intermediate.pem`. 

3. **JWT Vulnerability Auditing**: Audit all JWT files located in `/home/user/tokens/`. The directory contains several `.jwt` files. You must decode the header of each JWT and flag any token that attempts to bypass signature validation by setting the algorithm (`alg`) to `none` (case-insensitive).

Your Python script must execute these checks and output the results to a JSON file at `/home/user/audit_report.json` with the following exact structure:

```json
{
  "issuer_id": "<the_extracted_value_after_the_equals_sign>",
  "chain_valid": <true or false>,
  "vulnerable_tokens": ["<filename1.jwt>", "<filename2.jwt>"]
}
```

Notes:
- The `vulnerable_tokens` list should contain just the filenames (e.g., `token2.jwt`), sorted alphabetically.
- Do not use any external libraries outside of the standard library, `cryptography`, or tools natively available on standard Linux systems (like `openssl`, `readelf`, `strings`, etc., which you can call via `subprocess`).
- Once your script `/home/user/enforce_policy.py` is written, execute it so that `/home/user/audit_report.json` is generated.