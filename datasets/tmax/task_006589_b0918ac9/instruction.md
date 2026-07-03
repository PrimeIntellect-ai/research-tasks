You are a security engineer performing post-incident analysis and credential rotation. We discovered that our file upload handler was susceptible to a path traversal vulnerability. 

You have been provided with an application log file at `/home/user/upload.log` and an encrypted file containing new credentials at `/home/user/new_creds.aes`.

Write a Go program at `/home/user/remediate.go` (and execute it) to perform the following steps:

1. **Intrusion Detection**: Read `/home/user/upload.log`. Identify all log lines where the request path (the third space-separated field) contains the path traversal sequence `../`. Extract the source IP addresses (the first space-separated field) from these lines. Write the unique IP addresses to `/home/user/attacker_ips.txt`, sorted alphabetically, one per line.
2. **Sensitive Data Redaction**: The log file inadvertently captured AWS access keys. Find all instances of strings starting with `AKIA` followed by exactly 16 uppercase alphanumeric characters (A-Z, 0-9). Replace each 20-character matched string with exactly `[REDACTED]`. Save this cleaned log to `/home/user/upload_clean.log`. Maintain the original line breaks.
3. **File Integrity & Key Derivation**: Compute the SHA256 hash of the newly created `/home/user/upload_clean.log` file. 
4. **Decryption**: The file `/home/user/new_creds.aes` contains the rotated credentials, encrypted using AES-256-GCM. 
   - The 32-byte encryption key is the raw bytes of the SHA256 hash calculated in step 3 (i.e., decode the hexadecimal hash string into its 32-byte representation).
   - The first 12 bytes of `new_creds.aes` consist of the GCM nonce.
   - The remainder of the file is the ciphertext (which includes the GCM authentication tag).
   Decrypt the file and write the plaintext output to `/home/user/new_creds.txt`.

Ensure your Go script handles all steps automatically.