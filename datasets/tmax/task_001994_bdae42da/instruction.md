You are a security engineer tasked with rotating credentials and patching a legacy C++ backend service after a suspected breach. You need to perform the following operations:

1. **Code Audit & Patching (C++)**
   There is a C++ source file located at `/home/user/app/auth_service.cpp`. The code has two major vulnerabilities:
   - A CWE-89 (SQL Injection) vulnerability in the `getUserByToken` function.
   - A CWE-327 (Use of a Broken or Risky Cryptographic Algorithm) vulnerability in the `encryptData` function.
   
   Your task:
   - Identify the SQL injection and rewrite the query construction. Change the vulnerable string concatenation to use a parameterized statement placeholder. Specifically, replace the `query = ...` line with `std::string query = "SELECT * FROM users WHERE token = ?";` and add a comment `// Parameterized query` on the next line.
   - Identify the broken cryptography. The code currently uses `EVP_aes_256_ecb`. Modify it to use `EVP_aes_256_cbc`. Ensure the function signature and initialization accommodate a hardcoded IV of `0000000000000000` (16 bytes of '0') for the context initialization.
   - Save the patched file as `/home/user/app/auth_service_fixed.cpp`.

2. **Credential Rotation**
   The database configuration was compromised. The encrypted config is at `/home/user/secrets/db_config.enc`. It was encrypted using `aes-256-ecb` with the old hex key: `6f6c645f7365637265745f6b65795f31323334353637383930313233343536`.
   - Decrypt this file to retrieve the plaintext configuration.
   - Re-encrypt the plaintext configuration using `aes-256-cbc`.
   - Use the new hex key: `6e65775f7365637265745f6b65795f31323334353637383930313233343536`
   - Use the hex IV: `30303030303030303030303030303030`
   - Save the newly encrypted file to `/home/user/secrets/db_config_rotated.enc` (in raw binary format, not base64).

3. **SSH Hardening**
   The automated deployment system needs a new SSH key.
   - Generate an Ed25519 SSH keypair without a passphrase. Save the private key to `/home/user/.ssh/deploy_key`.
   - Create or append to `/home/user/.ssh/authorized_keys`. Add the newly generated public key, but you must harden it by prepending the following restrictions exactly: `command="/opt/deploy.sh",no-pty,no-port-forwarding ` (ensure there is a space before the `ssh-ed25519` part of the key).

4. **Certificate Chain Validation**
   We have received new deployment certificates in `/home/user/certs/`.
   - `root.crt` (Root CA)
   - `intermediate.crt` (Intermediate CA)
   - `server.crt` (Server Certificate)
   Verify the certificate chain using OpenSSL. Determine if `server.crt` is fully valid according to the provided intermediate and root certificates.
   Write the exact word `VALID` or `INVALID` to `/home/user/cert_status.txt` based on your findings.

Complete all steps and ensure the output files exist with the exact requested names and permissions.