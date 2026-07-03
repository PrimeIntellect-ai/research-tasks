You are a DevSecOps engineer performing a security audit and enforcing policy as code. 

During your scan, you discovered an old script at `/home/user/legacy_auth.py` that contains an encrypted SSH private key. The script was used to deploy to legacy servers, but it relies on a custom, weak encryption routine that uses a 4-digit numeric PIN as the key.

Your task is to:
1. Audit the encryption mechanism in `/home/user/legacy_auth.py`.
2. Write a Python script to brute-force the 4-digit PIN and recover the original SSH Ed25519 private key. You know the decrypted key must start with the standard OpenSSH private key header (`-----BEGIN OPENSSH PRIVATE KEY-----`).
3. Save the recovered, plaintext private key to `/home/user/.ssh/id_ed25519_recovered`.
4. Apply proper SSH hardening policies by setting the correct file permissions on the recovered private key file.
5. Identify the primary Common Weakness Enumeration (CWE) identifier associated with the use of a custom, weak, or broken cryptographic algorithm. Write ONLY the exact CWE ID (e.g., `CWE-123`) to `/home/user/cwe_finding.txt`.

Ensure your final recovered key file exists, contains the plaintext private key, and has the strict permissions required by SSH.