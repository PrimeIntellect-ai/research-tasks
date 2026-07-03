You are an AI assistant acting as a compliance analyst. We recently discovered that an internal service had a critical vulnerability: it accepted JSON Web Tokens (JWTs) with the `alg` (algorithm) header set to `none`, allowing attackers to bypass authentication and execute privileged commands.

Your task is to analyze the server logs, identify compromised administrative sessions, decrypt the actions the attacker took, and generate an audit trail. 

Here is what you need to do:
1. **Analyze the TLS Certificate:** The attacker encrypted their actions using a key derived from the server's public key. Extract the public key from the PEM-encoded certificate located at `/home/user/audit/server.crt`. Calculate the SHA-256 hash of this public key (in its DER format). The first 16 bytes of this SHA-256 hash constitute the AES-128 encryption key.
2. **Create a Rust Auditing Tool:** Initialize a new Rust project at `/home/user/audit_tool/`. Write a Rust program that reads the log file located at `/home/user/audit/logs/access.log`.
3. **Parse Security Logs:** The log file contains HTTP requests. Look for `Authorization: Bearer <token>` headers.
4. **Identify Forgeries:** Decode the JWTs (Base64Url decode the header and payload). Do NOT attempt to verify the signature. You are looking specifically for tokens where:
   - The decoded header contains `"alg":"none"`.
   - The decoded payload contains `"role":"admin"`.
5. **Decrypt the Audit Trail:** In the payload of these forged admin tokens, there is an `encrypted_action` field containing a hex-encoded string. Decrypt this string using AES-128 in ECB mode with no padding (or standard PKCS7 if you prefer, but the plaintext actions are exactly 16 bytes), using the 16-byte key derived in Step 1.
6. **Generate the Report:** For each forged admin token found, in the order they appear in the log, write the decrypted plaintext action to `/home/user/audit/compromised_actions.txt`. Each action should be on a new line.

Requirements:
- Ensure your Rust tool builds and runs successfully using `cargo run`.
- You may use standard Rust crates (e.g., `base64`, `serde_json`, `aes`, `hex`, `sha2`).
- The final output file `/home/user/audit/compromised_actions.txt` must contain exactly the decrypted actions, one per line, with no extra text.