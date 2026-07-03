You are a penetration tester reviewing intercepted traffic. You have acquired a directory of intercepted PEM files containing both X.509 certificates and RSA private keys. As part of the vulnerability analysis, you need to identify weakly generated keys, but you must strictly follow operational security guidelines regarding process isolation and data redaction.

Write a Bash script at `/home/user/process_intercepts.sh` that performs the following tasks:

1. Iterates over all `.pem` files in `/home/user/intercepts/`.
2. Identifies files containing weak RSA private keys. For this engagement, a "weak" key is defined as having exactly 1024 bits.
3. For security and sandboxing (to prevent accidental exfiltration by compromised parsers), every invocation of `openssl` to inspect the keys must be strictly isolated from the network using `unshare -n` (e.g., `unshare -n openssl rsa ...`).
4. For each identified weak key file, copy it to `/home/user/vuln_redacted/` keeping the same filename.
5. In the copied files in `/home/user/vuln_redacted/`, redact the actual private key material to prevent exposing sensitive data in your final report. You must replace all lines *between* `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----` (or `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`, depending on the format) with a single line containing exactly `[REDACTED]`. The header and footer lines must remain intact.

**Requirements:**
- The script must be executable.
- Do not hardcode the names of the files; the script must dynamically read the `/home/user/intercepts/` directory.
- The output files in `/home/user/vuln_redacted/` must contain the unredacted certificate block and the properly redacted private key block.