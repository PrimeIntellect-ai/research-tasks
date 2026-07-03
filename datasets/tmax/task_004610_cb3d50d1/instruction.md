You are a security engineer assigned to perform post-incident credential rotation and log analysis on a compromised internal server.

Your objectives are:
1. **Recover the Backup Password**: The previous administrator left a screenshot of the backup decryption password at `/app/passphrase.png`. Use optical character recognition (OCR) tools available on the system to extract this password. Strip any trailing whitespace.
2. **Decrypt the Backup**: The system backup is encrypted at `/home/user/backup.enc`. Decrypt it using OpenSSL (AES-256-CBC with PBKDF2) and the password you extracted. Save the decrypted output to `/home/user/backup.tar.gz`.
3. **SSH Hardening**: The SSH keys were compromised. Generate a new ED25519 SSH key pair at `/home/user/.ssh/id_ed25519` (with no passphrase). Then, create an SSH client configuration file at `/home/user/.ssh/config` that applies to all hosts (`Host *`), explicitly disables `PasswordAuthentication`, and specifies the new `IdentityFile`.
4. **TLS Certificate Rotation**: The server's TLS certificate was also compromised. Generate a new self-signed TLS certificate (`/home/user/server.crt`) and a new unencrypted 2048-bit RSA private key (`/home/user/server.key`). The certificate must be valid for 365 days and have the Common Name (CN) set to `internal.corp`.
5. **Log Sanitization Script**: The incident was caused by malicious HTTP requests. Write a Bash script at `/home/user/filter_logs.sh` that acts as a log sanitiser. 
   - The script must take exactly one argument: the path to a log file.
   - It must print to standard output ONLY the "clean" (benign) log entries.
   - It must filter out any "evil" log entries that contain common exploit payloads. Specifically, you must drop any line containing:
     - Cross-Site Scripting (XSS): `<script` or `javascript:` (case-insensitive)
     - Path Traversal: `../` or `..%2F`
     - SQL Injection: `UNION SELECT` or `1=1` (case-insensitive)
     - Shell Injection: `$(` or backticks (`` ` ``) or `wget `

Ensure your `filter_logs.sh` script is executable. You can use standard bash utilities (`grep`, `awk`, `sed`, etc.).