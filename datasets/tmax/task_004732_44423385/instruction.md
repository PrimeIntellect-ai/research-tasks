You are a compliance analyst responsible for generating secure audit trails and remediating a recent security incident. 

You have been provided with a server environment snapshot. Perform the following four tasks using Bash commands and scripts:

**1. Intrusion Detection (Process Snapshot Analysis)**
A rogue script may have leaked credentials via command-line arguments. We have created a snapshot of the `/proc` directory at `/home/user/proc_dump/`. Each subdirectory is a PID, containing a `cmdline` file where arguments are null-separated (just like the real `/proc/[pid]/cmdline`).
Write a script to scan this directory. Find any processes that were launched with an argument starting exactly with `--secret-token=`. 
Extract the PID and the token value. Save this list to `/home/user/audit_trail.txt` in the exact format:
`[PID]:[TOKEN]`
*(Example: `1099:mysecret123`)*
Sort the file numerically by PID.

**2. Audit Trail Encryption**
You must securely encrypt the audit trail for transmission. 
Encrypt `/home/user/audit_trail.txt` using `openssl` with the `aes-256-cbc` cipher and `-pbkdf2`. Use the symmetric passphrase stored in `/home/user/audit.key`. 
Save the encrypted output exactly to `/home/user/audit_trail.enc`.

**3. File Integrity Verification**
The application code is located in `/home/user/web_app/`. A manifest of expected SHA-256 hashes is provided in `/home/user/manifest.sha256`. 
Some files may have been tampered with or deleted by the rogue process. Verify the files against the manifest.
Create a file `/home/user/compromised_files.txt` containing the names of any files that are missing or have a hash mismatch. List only the filenames (e.g., `js/app.js`), one per line, sorted alphabetically.

**4. Content Security Policy (CSP) Remediation**
To prevent further data exfiltration, construct a strict CSP header.
Read the list of trusted domains from `/home/user/trusted_domains.txt`. 
Generate a file at `/home/user/csp_header.txt` containing exactly one line with the following format:
`Content-Security-Policy: default-src 'self'; script-src 'self' <domain1> <domain2> ...;`
*(Replace `<domain1> <domain2> ...` with a space-separated list of the domains found in `trusted_domains.txt` on a single line).*