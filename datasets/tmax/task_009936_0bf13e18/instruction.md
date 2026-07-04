You are a compliance analyst generating an automated audit trail for a web service. Recent vulnerability scans identified an open redirect vulnerability in the login flow (`/login?redirect=<url>`).

Your environment contains a web server access log at `/home/user/access.log`. You also have a partially completed C++ log scanner at `/home/user/audit_scanner.cpp`.

Your task is to complete the following:

1. **Fix the Vulnerability Scanner (C++)**: 
   The current C++ program parses the log but flags *all* redirect attempts as vulnerabilities. Modify `/home/user/audit_scanner.cpp` so that it only identifies a redirect as an "open redirect vulnerability" if the `redirect` query parameter value starts exactly with `http://` or `https://`. Relative paths (e.g., `/dashboard`) should be ignored.

2. **Add Cryptographic Hashing**:
   Modify the C++ program to compute the SHA-256 hash (in lowercase hexadecimal) of the extracted vulnerable redirect URL. Use the OpenSSL library for this computation.

3. **Generate the Audit Report**:
   Compile the C++ program. You will need to link against the OpenSSL libraries. Run the compiled program and save its standard output to `/home/user/audit_report.csv`.
   The output must be strictly in CSV format with no headers: `IP_Address,Vulnerable_URL,URL_SHA256_Hex`

4. **SSH Hardening for Audit Transport**:
   The automated pipeline requires a dedicated SSH key to securely transfer this audit report off-site. Generate a new `ed25519` SSH key pair saved exactly at `/home/user/.ssh/audit_key` with an empty passphrase.

**Constraints & Hints**:
- The log format is standard combined: `IP - - [Date] "GET /path HTTP/1.1" Status Size`
- You may install any necessary C++ OpenSSL development headers via the package manager if they are missing.
- Only flag lines containing `/login?redirect=` where the value is an absolute HTTP/HTTPS URL.