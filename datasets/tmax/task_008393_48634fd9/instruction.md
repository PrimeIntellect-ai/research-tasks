You are a security engineer tasked with auditing and rotating credentials for a legacy backup system. 

There are several service scripts located in the directory `/home/user/services/`. You need to perform the following steps:

1. **Privilege Escalation Auditing:** Audit the `/home/user/services/` directory to identify a script that poses a local privilege escalation risk due to being world-writable (modifiable by any user).
2. **Password Cracking:** Inside this vulnerable script, you will find a hardcoded variable named `SECRET_HASH` containing an MD5 hash of the legacy service password. The legacy password is known to be the word `admin` followed by exactly four digits (e.g., `admin0000` through `admin9999`). Crack this hash. 
   - Write the cracked plaintext password to `/home/user/cracked_password.txt`.
3. **Credential Rotation:** We are rotating the password to a new value: `SecureBackup2024!`. 
   - Replace the old MD5 hash in the script with the **SHA-256** hash of the new password. 
   - Rename the variable in the script from `SECRET_HASH` to `NEW_SECRET_HASH`.
4. **Remediation:** Fix the privilege escalation vulnerability by removing the world-writable permissions from the script (change its permissions to `755`).
5. **Checksum Verification:** Compute the SHA-256 checksum of the newly modified and secured script. 
   - Write this checksum to `/home/user/audit_log.txt` strictly in the following format:
     `CHECKSUM: <computed_sha256_hash>`

Ensure all final files (`cracked_password.txt`, `audit_log.txt`, and the modified script) exist and contain the exact requested values. You may use any programming language or shell utilities available to complete these tasks.