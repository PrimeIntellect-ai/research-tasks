You are acting as a compliance analyst for a financial institution. You need to generate an automated audit trail report that evaluates a specific web server's TLS configuration, its Content Security Policy (CSP) headers, and demonstrates the vulnerability of a legacy proprietary hash function still in use. 

All your work should be done in `/home/user`.

You are provided with the following files (assume they exist in `/home/user/`):
1. `server.crt`: The PEM-encoded X.509 certificate used by the server.
2. `headers.log`: A text file containing the raw HTTP response headers returned by the server.
3. `weak_hash.c`: A C file containing a legacy 16-bit hashing function (`uint16_t weak_hash(const char* input);`) that the security team wants to deprecate.

Your task is to perform the following analysis and compile the results into a single JSON audit report at `/home/user/audit_report.json`.

**Phase 1: TLS Certificate Management & Hashing**
Extract the SHA-256 fingerprint of the certificate in `server.crt`.

**Phase 2: Content Security Policy Enforcement**
Analyze `headers.log` to find the `Content-Security-Policy` header. Determine if the `script-src` directive explicitly contains `'unsafe-eval'`. 

**Phase 3: Cryptanalysis (Collision Finding)**
The security team needs proof that the hash function in `weak_hash.c` is vulnerable to collisions. 
Write a C program (or script) to find two *strictly different* printable ASCII strings (each between 3 and 15 characters long) that produce the exact same 16-bit integer output when passed to `weak_hash()`. 

**Phase 4: Audit Trail Generation**
Create `/home/user/audit_report.json` with the exact following structure:
```json
{
  "cert_fingerprint_sha256": "<The extracted SHA-256 fingerprint, uppercase with colons>",
  "csp_contains_unsafe_eval": <true or false (boolean)>,
  "legacy_hash_collision": [
    "<collision_string_1>",
    "<collision_string_2>"
  ]
}
```

Constraints:
- The `cert_fingerprint_sha256` must exactly match the standard OpenSSL output format (e.g., `SHA256 Fingerprint=...` but ONLY the hex string with colons: `AB:CD:12...`).
- The strings in the collision array must not be equal, but must hash to the exact same value using the logic in `weak_hash.c`.