You are acting as a security engineer responding to a recent breach. An attacker exploited a path traversal vulnerability in a file upload handler, allowing them to read sensitive files and credentials. You must perform credential rotation, data redaction, and simulated SSH hardening. 

Perform the following tasks using Bash. All work should be done within the `/home/user/incident_response/` directory.

**Phase 1: Log Redaction**
The file `/home/user/incident_response/access.log` contains traces of the path traversal attacks, but it also accidentally logged user passwords and API tokens.
Write a Bash script at `/home/user/incident_response/redact.sh` that reads `access.log` and redacts sensitive data as follows:
- Replace any occurrence of `password=<any alphanumeric string>` with `password=REDACTED`
- Replace any occurrence of `Bearer <any base64-like string with dots/dashes/underscores>` with `Bearer REDACTED`
Run your script and save the output to `/home/user/incident_response/access_redacted.log`.

**Phase 2: Configuration Decryption and Rotation**
The attacker compromised the symmetric encryption key used for backups. 
1. Decrypt the file `/home/user/incident_response/config.enc`. It was encrypted using OpenSSL `aes-256-cbc` with the password `compromised_pass_123` (using `-pbkdf2`).
2. The decrypted configuration file contains several key-value pairs. Find the line starting with `DB_PASSWORD=` and change its value to `NewSecureDbPass2024!`. Save this modified plaintext to `/home/user/incident_response/config_updated.txt`.
3. Re-encrypt this updated plaintext file using OpenSSL `aes-256-cbc` with the new password `SecureRotation_456` (using `-pbkdf2`). Save the encrypted file to `/home/user/incident_response/config_new.enc`.

**Phase 3: SSH Hardening and Key Rotation**
We need to harden the SSH configuration and rotate the exposed keys.
1. A local copy of the SSH daemon configuration is located at `/home/user/incident_response/sshd_config`. Modify this file directly to ensure the following directives are set exactly as shown (uncomment them or add them if they don't exist, and remove conflicting lines):
   - `PermitRootLogin no`
   - `PasswordAuthentication no`
2. Generate a new SSH Ed25519 keypair with no passphrase. Save the private key exactly to `/home/user/incident_response/new_keys/id_ed25519` (the public key will be generated automatically in the same directory).

Do not change the ownership or permissions beyond what is standard for SSH keys. Ensure all paths and filenames match exactly.