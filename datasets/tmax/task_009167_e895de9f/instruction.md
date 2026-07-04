You are acting as a security auditor performing a review of a deployment environment. You need to verify access controls, check artifact integrity, and fix a broken authentication validation script.

Your tasks are divided into three phases. All work must be done within the `/home/user` directory.

**Phase 1: SSH Hardening and Key Management**
In the `/home/user/ssh_audit/` directory, you will find several private SSH keys. 
1. You must analyze these keys and identify any that are insecure. A key is considered insecure if:
   - It is an RSA key with a length of less than 2048 bits.
   - It is a DSA key.
   - The file permissions are broader than `0600` (meaning they can be read or written by group/others).
2. Move all insecure private keys to the `/home/user/quarantine_keys/` directory (create this directory if it doesn't exist).
3. For the remaining secure keys, compute their SHA256 fingerprints. Write the fingerprints of the secure keys to `/home/user/secure_keys.txt`. Format the file with one fingerprint per line, formatted exactly as output by `ssh-keygen -l` (e.g., `2048 SHA256:... user@host (RSA)`).

**Phase 2: Artifact Integrity (Cryptographic Checksums)**
In the `/home/user/artifacts/` directory, there are several binary files and a `manifest.sha256` file containing their expected cryptographic hashes.
1. Verify the checksums of all `.bin` files against the manifest.
2. Identify which files have been tampered with (their checksums do not match the manifest).
3. Write the base filenames (e.g., `file2.bin`) of the modified artifacts to `/home/user/corrupted_files.txt`, one per line.

**Phase 3: Authentication Flow Testing**
In the `/home/user/auth/` directory, there is a Python script `login_check.py`, a `secret.key` file, and a `requests.json` file. The Python script simulates a token validation flow.
1. The script requires that `secret.key` has strict permissions to run. Ensure `secret.key` has `0600` permissions.
2. The `login_check.py` script has two critical security flaws in its implementation:
   - It incorrectly uses MD5 instead of SHA256 for the HMAC calculation.
   - It uses a basic string comparison `==` instead of a timing-attack resistant function for the signature verification.
3. Fix the `login_check.py` script to use `hashlib.sha256` and Python's `hmac.compare_digest`.
4. Run the fixed script. It will print the username of the single valid request.
5. Write that valid username to `/home/user/valid_user.txt`.