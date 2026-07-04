You are acting as a security engineer who has just inherited an older web application environment. The previous administrator left behind some poorly configured SSH settings and a custom, weak authentication token generator. You need to rotate the credentials, secure the environment, and recover the old database password.

Please complete the following tasks:

1. **SSH Hardening & Key Management:**
   - The directory `/home/user/.ssh` and the private key `/home/user/.ssh/id_rsa` currently have dangerously open permissions. Fix their permissions to standard secure values (directories should be `700`, private keys should be `600`).
   - Generate a new `ed25519` SSH keypair for future deployments. Save it exactly at `/home/user/.ssh/deploy_key` with no passphrase.

2. **Payload Decoding & Cryptanalysis:**
   - The previous admin used a custom, weak encoding scheme for authentication payloads, defined in `/home/user/legacy_auth.py`.
   - There is a file at `/home/user/admin_payload.b64` which contains a base64-encoded string. This string was generated using the logic in `legacy_auth.py`.
   - Analyze `legacy_auth.py` to understand the weak custom encryption (a single-byte XOR cipher).
   - Write a Python script to decode the contents of `/home/user/admin_payload.b64`. The decrypted payload is in the format `username:password`.

3. **Reporting:**
   - Create a final report file at `/home/user/rotation_summary.txt`.
   - The file must contain exactly three lines in the following format:
     Line 1: The recovered password from the decoded payload.
     Line 2: The entire public key string from your newly generated deploy key (the contents of `/home/user/.ssh/deploy_key.pub`).
     Line 3: A newly generated token for the username `system_admin`, created using the exact same weak encoding logic found in `/home/user/legacy_auth.py` (so the legacy systems can still authenticate during the migration window).

Ensure all requested files are created at the exact paths specified and with the correct permissions.