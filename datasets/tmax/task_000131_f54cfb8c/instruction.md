You are a DevSecOps engineer tasked with enforcing policy-as-code baselines on a local application deployment. You need to write a Bash script that audits various components of the application for security vulnerabilities.

Create a Bash script at `/home/user/audit_policy.sh` and execute it. The script must perform the following checks and write the results to `/home/user/audit_report.txt`. 

1. **JWT Algorithm Validation (Encryption/Decryption primitives):**
   The directory `/home/user/tokens/` contains several JSON Web Tokens (files ending in `.jwt`). These tokens consist of three base64url-encoded parts separated by dots.
   You must decode the header (the first part) of each token and check if the cryptographic algorithm specified is "none" (i.e., `{"alg":"none",...}`).
   For every vulnerable token found, append a line to `/home/user/audit_report.txt` in the exact format:
   `JWT_VULN: <filename>` (e.g., `JWT_VULN: token_b.jwt`)

2. **Injection & XSS Log Analysis:**
   The file `/home/user/logs/access.log` contains HTTP request logs. You must identify lines that contain basic Cross-Site Scripting (XSS) or SQL Injection (SQLi) payloads.
   Specifically, flag any line containing the exact string `<script>` OR the exact string `UNION SELECT`.
   For each vulnerable line, append to the report:
   `INJECTION_VULN: line <line_number>` (e.g., `INJECTION_VULN: line 14`)

3. **Certificate Chain Validation:**
   The application uses a certificate located at `/home/user/certs/server.pem`. Verify this certificate against the Certificate Authority (CA) provided at `/home/user/certs/ca.pem`. 
   If the certificate fails validation against this specific CA, append to the report:
   `CERT_VULN: server.pem is invalid`

4. **File Permission Control:**
   The directory `/home/user/keys/` contains sensitive cryptographic keys. Enforce the principle of least privilege: these files must only be readable and writable by the owner (equivalent to `chmod 600`). No permissions should be granted to group or others.
   For any file violating this strict permission requirement, append to the report:
   `PERM_VULN: <filename>` (e.g., `PERM_VULN: app_key.pem`)

**Constraints & Notes:**
- All outputs must be appended to `/home/user/audit_report.txt`.
- Do not include the full path in the filenames printed to the report (e.g., use `token2.jwt`, not `/home/user/tokens/token2.jwt`).
- You may use standard Linux utilities available in Bash (e.g., `jq`, `base64`, `openssl`, `awk`, `grep`, `stat`, `find`). Note that base64url encoding uses `-` and `_` instead of `+` and `/`, so you may need to sanitize the string before passing it to standard `base64 -d`.
- Order of operations in the output file does not matter, as long as all required lines are present.
- Ensure your script `/home/user/audit_policy.sh` is executable and executed before you finish.