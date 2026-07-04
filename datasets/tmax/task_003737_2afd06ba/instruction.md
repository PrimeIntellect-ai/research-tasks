You are acting as a security auditor reviewing a misconfigured TLS/SSL directory. 

The directory `/home/user/web_certs` contains a public certificate (`server.crt`) and two encrypted private key backups (`backup_alpha.enc` and `backup_beta.enc`). A junior administrator forgot which backup corresponds to the active certificate and left the directory with overly permissive file access rights.

Your task is to restore the secure state of this directory by performing the following steps using standard Bash and OpenSSL commands:

1. **Decrypt the Backups:** 
   Both `.enc` files are encrypted using OpenSSL AES-256-CBC with the `-pbkdf2` option. The passphrase for both is `S3cr3tKeyB4ckup`. Decrypt both files.

2. **Verify Integrity and Match:**
   Compare the RSA modulus of the decrypted keys with the RSA modulus of `server.crt`. Identify which decrypted key mathematically matches the certificate.

3. **Restore the Correct Key:**
   Save the matching decrypted private key as `/home/user/web_certs/server.key`. 
   Delete the non-matching decrypted key, as well as the original `backup_alpha.enc` and `backup_beta.enc` files.

4. **Enforce Access Control:**
   - Apply strict `600` permissions to any file ending in `.key` in the `/home/user/web_certs` directory.
   - Apply `644` permissions to the public certificate `server.crt`.

5. **Generate an Audit Report:**
   Create a report file at `/home/user/audit_report.txt` exactly matching the following format:
   - **Line 1:** The text `MATCHED KEY SHA256:` followed by the SHA-256 checksum of the restored `server.key` file (just the hash, do not include the filename).
   - **Line 2:** The text `MODULUS MD5:` followed by the MD5 hash of the RSA modulus of `server.key`. (e.g., `MODULUS MD5: d41d8cd98f00b204e9800998ecf8427e`)
   - **Line 3 and onwards:** The absolute file path and octal permissions of every file currently in `/home/user/web_certs`, formatted using `stat -c "%n %a"` and sorted alphabetically by file path.

Ensure your final directory state and audit report are perfectly formatted.