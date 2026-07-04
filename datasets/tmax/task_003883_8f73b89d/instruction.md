You are a security engineer responsible for rotating credentials on a legacy server. An old, encrypted SSH private key was recently discovered, but the passphrase was lost. Fortunately, you have a SHA256 hash of the passphrase and know it consists of exactly 4 lowercase English letters (e.g., 'aaaa' to 'zzzz'). 

Your task involves several steps spanning password recovery, credential rotation, and log redaction.

**Step 1: Password Recovery (Brute Force)**
A text file `/home/user/pass_hash.txt` contains the SHA256 hash (in hex) of the passphrase. 
Write a C program at `/home/user/cracker.c` that brute-forces this hash to recover the 4-letter passphrase. You may use the OpenSSL crypto library (`-lcrypto`). 

**Step 2: Key Verification and Rotation**
Use the recovered passphrase to decrypt the old SSH private key located at `/home/user/old_key.pem`. Ensure you can read its decrypted contents (you don't need to save the decrypted version).
Next, generate a new, unencrypted ED25519 SSH key pair. Save the private key exactly to `/home/user/new_key` (and the public key will naturally be `/home/user/new_key.pub`).

**Step 3: Sensitive Data Redaction**
During an audit, it was discovered that a log file `/home/user/audit.log` accidentally leaked both the plaintext passphrase and the old encrypted private key. 
You must redact `/home/user/audit.log` in-place by:
1. Replacing all occurrences of the recovered 4-letter plaintext passphrase with the exact string `[REDACTED_PASS]`.
2. Replacing the entire old encrypted private key block (everything from `-----BEGIN ENCRYPTED PRIVATE KEY-----` to `-----END ENCRYPTED PRIVATE KEY-----`, including those header/footer lines and all lines in between) with the exact string `[REDACTED_KEY]`.

**Step 4: Output Summary**
Create a summary file at `/home/user/rotation_summary.txt` with exactly the following format:
```
Old Passphrase: <recovered_passphrase>
New Public Key: <exact_contents_of_/home/user/new_key.pub>
```
(Note: The new public key content should be on a single line as it appears in the `.pub` file).

**Constraints:**
- Do not change the permissions of the directory unless necessary.
- The C program must be written by you and compile successfully with `gcc`. 
- Make sure `/home/user/audit.log` is updated in-place or replaced at the same path.