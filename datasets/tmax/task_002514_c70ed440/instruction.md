You are acting as a compliance analyst tasked with securing an automated audit reporting system. Currently, the system has multiple security flaws, including leaking credentials via command-line arguments, lacking secure communication certificates, and relying on insecure authentication methods.

Your objective is to fix these issues by completing the following four phases:

**Phase 1: Remediation of Credential Leak & Log Redaction**
There is a Python script at `/home/user/audit_runner.py`. Currently, it executes a subprocess call to `/home/user/scanner.sh`, passing a sensitive API token as a command-line argument. This is a severe security risk as the token becomes visible in `/proc`.
1. Modify `/home/user/audit_runner.py` so that the API token is no longer passed as a command-line argument to the subprocess. Instead, the script must pass the token to the subprocess via an environment variable named `SCANNER_TOKEN`. (The `scanner.sh` script has already been updated to look for this environment variable).
2. The `audit_runner.py` script writes logs. You must implement a redaction mechanism inside the Python script so that before it writes to `/home/user/audit_log.txt`, any occurrence of the API token string is replaced with the exact string `[REDACTED]`.
3. Run your modified script: `python3 /home/user/audit_runner.py --token "super_secret_audit_token_991"`. Ensure the resulting `/home/user/audit_log.txt` contains the output, properly redacted.

**Phase 2: Payload Decoding**
An encrypted audit payload was previously encoded in base64 and saved at `/home/user/payload.b64`. 
Decode this file and save the raw plaintext output to `/home/user/payload.txt`.

**Phase 3: SSH Key Management & Hardening**
The system currently connects to audit targets using passwords. You need to enforce key-based authentication.
1. Generate an Ed25519 SSH keypair without a passphrase. Save the private key exactly at `/home/user/.ssh/audit_key`.
2. Create an SSH configuration file at `/home/user/.ssh/config`. Add a configuration block for the host `audit-target` with the following parameters:
   - HostName: 127.0.0.1
   - User: audituser
   - IdentityFile: /home/user/.ssh/audit_key
   - PasswordAuthentication: no
3. Ensure the `.ssh` directory and its contents have the correct, secure file permissions.

**Phase 4: TLS/SSL Certificate Management**
The audit log aggregator requires a TLS connection, but it lacks a certificate.
1. Create a directory `/home/user/certs/`.
2. Generate a self-signed X.509 certificate and its corresponding RSA private key (2048-bit). 
3. The certificate must have the Common Name (CN) set exactly to `audit.local`.
4. Save the private key to `/home/user/certs/audit_server.key` and the certificate to `/home/user/certs/audit_server.crt`.

Ensure all files are created in the exact paths specified above.