You are acting as a security auditor for a staging environment of a local web application. The development team has left the environment in an insecure state, and you need to secure it using Bash commands and scripts.

Complete the following phases to secure the environment:

**Phase 1: TLS/SSL Certificate Management**
The staging server needs to test HTTPS, but currently lacks certificates.
1. Create a directory `/home/user/certs`.
2. Generate a self-signed RSA 2048-bit certificate and private key.
3. The Common Name (CN) must be `staging.local`.
4. Save the certificate as `/home/user/certs/server.crt` and the key as `/home/user/certs/server.key`.
5. Ensure the key `/home/user/certs/server.key` has strict `600` permissions.

**Phase 2: File Permission and Access Control**
The web root directory `/home/user/web_root` has been left with insecure permissions (e.g., world-writable files, executable static assets).
1. Set all directories inside (and including) `/home/user/web_root` to `755`.
2. Set all files inside `/home/user/web_root` to `644`.

**Phase 3: Content Security Policy (CSP) Enforcement**
The main entry point, `/home/user/web_root/index.html`, lacks a Content Security Policy.
1. Inject the following meta tag exactly into `/home/user/web_root/index.html` immediately after the `<head>` tag:
`<meta http-equiv="Content-Security-Policy" content="default-src 'self';">`

**Phase 4: Sensitive Data Redaction**
The application logs at `/home/user/logs/app.log` contain sensitive credit card numbers in the format `XXXX-XXXX-XXXX-XXXX`. 
1. Write a Bash script at `/home/user/redact.sh` that reads `/home/user/logs/app.log`.
2. It must redact all credit card numbers by replacing the first 12 digits with `X`s, preserving the dashes and the last 4 digits. (e.g., `1234-5678-9012-3456` becomes `XXXX-XXXX-XXXX-3456`).
3. The script should output the redacted content to `/home/user/logs/app_redacted.log`.
4. Make `/home/user/redact.sh` executable and run it.

**Phase 5: Audit Summary**
Create a summary file at `/home/user/audit_summary.txt` with exactly four lines:
Line 1: The MD5 hash of `server.crt` (just the hash, no filename).
Line 2: The octal permissions of `/home/user/web_root/index.html` (e.g., 644).
Line 3: The number of redacted lines in `app_redacted.log` (count of lines containing `XXXX-XXXX-XXXX-`).
Line 4: The string `AUDIT_COMPLETE`.