You are a security auditor tasked with fixing vulnerabilities and creating an automated audit script for a critical application environment. 

The application is located in `/home/user/app_env`. You must write a Bash script at `/home/user/audit_and_fix.sh` that takes exactly one argument (the target base directory, e.g., `/home/user/app_env`) and performs the following security remediations and audits:

1. **File Integrity Verification:**
   Inside the target directory, there is a file named `known_hashes.txt` containing the expected SHA256 checksums of the files in the `bin/` subdirectory (in standard `sha256sum` output format).
   Your script must verify the hashes of the files in `<target_dir>/bin/`. 
   If any file fails the verification (the hash doesn't match), append its absolute path to `/home/user/compromised_files.txt`.

2. **Privilege Escalation Auditing:**
   Scan the entire target directory recursively for files that have either the SUID bit set, the SGID bit set, or are world-writable (others have write permission).
   For any such file found:
   - Append its absolute path to `/home/user/permission_violations.txt`.
   - Automatically remediate the file by removing the SUID, SGID, and world-writable permissions (but leave other permissions intact).

3. **Sensitive Data Redaction:**
   Scan all files in `<target_dir>/logs/` for leaked API keys. 
   An API key is formatted exactly as `API_KEY=` followed by exactly 16 alphanumeric characters (e.g., `API_KEY=aB3dE6gH1jK2mN4p`).
   Modify the files in-place to redact the key, changing the 16-character string to exactly `REDACTED` (i.e., it should become `API_KEY=REDACTED`).

4. **Content Security Policy Enforcement:**
   Check the configuration file `<target_dir>/config/app.conf`. 
   If it does not contain a line with the exact string `Header set Content-Security-Policy "default-src 'self';"`, append this exact line to the end of the file.

Write the script and then run it on `/home/user/app_env` to secure the environment. Ensure `/home/user/compromised_files.txt` and `/home/user/permission_violations.txt` are created properly (they should be empty or not exist before your script runs, and contain one absolute path per line if violations are found). Sort the output lines in the `.txt` files alphabetically.

Ensure your script `/home/user/audit_and_fix.sh` is executable.