You are acting as a Security Auditor for a legacy Linux environment. You need to perform an automated audit, fix basic SSH key hygiene issues, and securely extract and encrypt a sensitive log file for offline analysis.

Your task consists of three phases. Ensure all final output files are placed exactly where specified.

### Phase 1: Permission Audit
A directory containing system backups is located at `/home/user/backup_data`. Some files in this directory have been misconfigured with global/world-readable permissions (e.g., `o+r`).
1. Find all files in `/home/user/backup_data` (and its subdirectories) that are world-readable.
2. Output *only the basenames* (not the full paths) of these files into `/home/user/world_readable.txt`, one per line, sorted alphabetically.

### Phase 2: SSH Key Hardening
A directory containing SSH keys is located at `/home/user/ssh_keys`. SSH private keys must not be accessible to anyone other than the owner.
1. Identify any files in `/home/user/ssh_keys` that have permissions broader than `600` (i.e., accessible by group or others).
2. Change the permissions of these specific over-permissive files to `600`.
3. Output *only the basenames* of the files you modified into `/home/user/fixed_keys.txt`, one per line, sorted alphabetically.

### Phase 3: Log Redaction and Encryption Tool
A system log file at `/home/user/system.log` contains sensitive data that must be redacted before it can be analyzed. Write a Go program at `/home/user/redactor.go` that does the following:

1. **Read** `/home/user/system.log`.
2. **Redact Sensitive Data:**
   * **Passwords:** Any line containing the exact string `Password: ` followed by any characters until the end of the line must have the characters after the space replaced with `[REDACTED]`. (Example: `User login Password: mySecret123` becomes `User login Password: [REDACTED]`).
   * **SSH Private Keys:** Any multiline block starting exactly with `-----BEGIN OPENSSH PRIVATE KEY-----` and ending exactly with `-----END OPENSSH PRIVATE KEY-----` (inclusive of the header and footer lines) must be entirely replaced by the single string `[PRIVATE KEY REDACTED]`.
3. **Encrypt the Redacted Text:**
   * Read a 32-byte AES key from `/home/user/encryption_key.bin`.
   * Encrypt the redacted log data using AES-GCM.
   * Generate a random 12-byte nonce for the encryption.
   * The final output must consist of the 12-byte nonce followed immediately by the AES-GCM ciphertext.
4. **Write** the final binary output to `/home/user/secure_audit.enc`.

Compile and run your Go program to generate `/home/user/secure_audit.enc`.