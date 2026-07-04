You are a penetration tester performing a security audit and post-exploitation analysis on a target machine. You have discovered a locked vault containing SSH keys, along with the custom Python script the system administrators used to encrypt it.

Your objective is to audit the script, decrypt the vault, verify the integrity of its contents, and securely provision the extracted SSH key.

Here are the files provided to you in `/home/user/`:
1. `/home/user/key_gen.py`: A custom script used by the administrators to derive encryption keys and Initialization Vectors (IVs) for their backups.
2. `/home/user/password.txt`: A file containing the plaintext passphrase used for the vault.
3. `/home/user/vault.enc`: The AES-256-CBC encrypted tar archive containing the SSH keys.
4. `/home/user/manifest.sha256`: A file containing the expected SHA-256 checksums for the contents of the vault.

Perform the following tasks:

**Step 1: Code Auditing (CWE Identification)**
Audit `/home/user/key_gen.py`. Identify the specific MITRE CWE (Common Weakness Enumeration) ID representing the primary security flaw in how the Initialization Vector (IV) or key material is generated in this script. 
Write the exact CWE ID (e.g., `CWE-123`) to `/home/user/cwe.txt`.

**Step 2: Decryption**
Analyze the logic in `/home/user/key_gen.py` to understand how the AES-256-CBC key and IV were generated using the passphrase in `/home/user/password.txt`. Write a Python script to decrypt `/home/user/vault.enc` using the `cryptography` library. 
Save the decrypted archive as `/home/user/vault.tar`.
Extract the contents of `/home/user/vault.tar` into the directory `/home/user/vault/`.

**Step 3: Cryptographic Hashing & Integrity**
The target system's storage is unreliable. Verify the SHA-256 checksum of every file extracted in `/home/user/vault/` against the provided `/home/user/manifest.sha256`.
Identify any file whose hash does not match the manifest (indicating corruption or tampering) and completely delete it from the `/home/user/vault/` directory.

**Step 4: SSH Hardening**
After removing the corrupted files, you will be left with a valid SSH private key (ending in `.pem`) in the `/home/user/vault/` directory. 
Copy this valid private key to `/home/user/target_rsa`. 
Apply the strictly necessary filesystem permissions to `/home/user/target_rsa` so that the SSH client will accept it without throwing a "bad permissions" error.

Constraint: Ensure you use Python for the decryption and verification logic where appropriate, though shell commands can be used for file manipulation and permissions.