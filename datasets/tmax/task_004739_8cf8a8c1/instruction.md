You are a compliance analyst responding to a security incident. An attacker compromised a web server and deployed a custom data-exfiltration binary, leaking SSH keys and proprietary tracking credentials into the web application's audit logs.

Your goal is to prepare a sanitized audit trail for compliance review, harden the local SSH configuration to prevent future lateral movement, and analyze the malware.

**Step 1: Extract the Archive PIN**
We captured a screenshot of the attacker's terminal, located at `/app/evidence.png`. Use OCR (e.g., `tesseract`) to extract the 6-digit decryption PIN from this image.

**Step 2: Reverse Engineer the Malware**
An encrypted archive containing the malware is at `/app/malware.zip`. 
1. Unzip it using the PIN extracted in Step 1.
2. Inside, you will find a compiled binary `exfil.bin`.
3. Reverse engineer/inspect this binary to locate the exact format of the proprietary tracking credentials the attacker was targeting. You will find a plaintext string formatted exactly as `EXFIL_PATTERN: <regex_pattern>`. Note this regex pattern.

**Step 3: SSH Hardening**
Prepare a secure SSH environment for the audit team:
1. Generate a new ed25519 SSH keypair at `/home/user/.ssh/audit_id_ed25519` (no passphrase).
2. Create an SSH client configuration file at `/home/user/.ssh/config` with the following hardened settings for `Host *`:
   - Enforce the use of the generated key (`IdentityFile`).
   - Disable password authentication (`PasswordAuthentication no`).
   - Restrict ciphers to `chacha20-poly1305@openssh.com`.

**Step 4: Build the Log Sanitizer**
Write a redaction script at `/home/user/sanitizer.py`. The script must take an input log file path as its first CLI argument and output the sanitized log to `stdout`.

Redaction Rules:
1. **Proprietary Credentials:** Any string matching the exact regex pattern extracted in Step 2 must be replaced with the literal string `[REDACTED_CRED]`.
2. **SSH Private Keys:** Any entire SSH private key block (everything from `-----BEGIN OPENSSH PRIVATE KEY-----` to `-----END OPENSSH PRIVATE KEY-----`, including the headers, footers, and all base64 lines in between) must be replaced with the literal string `[REDACTED_KEY]`.

**Validation:**
We have provided two testing corpora:
- `/app/corpus/clean/`: Contains normal web logs and system events. Your sanitizer MUST NOT alter any text in these files.
- `/app/corpus/evil/`: Contains logs where credentials and SSH keys were leaked. Your sanitizer MUST successfully redact 100% of the proprietary credentials and SSH keys, matching the rules above.

Our automated verifier will execute:
`python3 /home/user/sanitizer.py <file>`
on a hidden set of clean and evil logs. To pass, you must achieve 100% clean preservation and 100% evil redaction.