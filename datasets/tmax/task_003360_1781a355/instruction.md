You are acting as a compliance analyst tasked with auditing a legacy binary and generating a secure audit trail.

We have discovered a suspicious binary executable located at `/home/user/vulnerable_service.bin`. 

Your objective is to perform the following steps:

1. **Binary Analysis & Pattern Matching**: Analyze the ELF binary `/home/user/vulnerable_service.bin` to find a hardcoded SHA-256 hash. The hash is stored as a string directly immediately following the exact prefix `AUTH_SIG:`. 

2. **Password Cracking**: The extracted SHA-256 hash corresponds to a 4-character lowercase English word. Write a Python script to brute-force and recover this plaintext password.

3. **SSH Hardening & Key Management**: 
   - Generate a new SSH key pair of type `ed25519`.
   - Save the private key to `/home/user/compliance_key`.
   - The private key MUST be protected with a passphrase. Set the passphrase to the exact plaintext password you cracked in Step 2.
   - Add the generated public key to `/home/user/.ssh/authorized_keys`.
   - Ensure that the `.ssh` directory and `authorized_keys` file have the correctly hardened Linux file permissions (700 for the directory, 600 for the keys file).

4. **Exploit Crafting & Audit Trail Generation**:
   - Write a Python script at `/home/user/generate_audit.py`.
   - When run, this script must generate a JSON file at `/home/user/audit_report.json` with the following exact keys and values:
     - `"extracted_hash"`: The SHA-256 hash string you extracted.
     - `"cracked_password"`: The plaintext password you recovered.
     - `"ssh_key_type"`: The string `"ed25519"`.
     - `"crafted_payload"`: A simulated exploit payload string consisting of exactly 64 uppercase "A"s followed immediately by the cracked password (e.g., `"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAword"`).

Complete all steps above and ensure the JSON file `/home/user/audit_report.json` is correctly formatted and generated.