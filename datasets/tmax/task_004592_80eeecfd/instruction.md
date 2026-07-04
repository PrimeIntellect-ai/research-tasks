You are a DevSecOps engineer tasked with enforcing security policies and remediating vulnerabilities in a legacy application bundle. You have been provided with an application directory `/home/user/app` and some security artifacts. Your goal is to remediate code vulnerabilities, fix access controls, crack a compromised admin hash to verify exposure, and generate an integrity audit log.

Perform the following tasks:

1. **Password Cracking (Exposure Verification):**
   An attacker dumped the admin password hash. The MD5 hash is stored in `/home/user/admin.hash`. A custom wordlist is provided at `/home/user/wordlist.txt`.
   - Crack the hash using the provided wordlist.
   - Save ONLY the plaintext password in `/home/user/cracked_password.txt`.

2. **Open Redirect Remediation:**
   The application uses a Python script for routing. The file `/home/user/app/login.py` contains a function `get_redirect_url(next_param)` that currently just returns whatever string is passed to it, causing an Open Redirect vulnerability.
   - Modify `/home/user/app/login.py`.
   - Update the `get_redirect_url(next_param)` function so that it validates the `next_param`.
   - The function must return `next_param` ONLY IF it is a relative path starting with exactly one slash (e.g., `/dashboard`). If it starts with `//` (protocol-relative), does not start with `/`, or is `None`/empty, the function must return the safe default string `'/home'`.

3. **File Permissions & Access Control:**
   The file `/home/user/app/config.json` contains plain-text API tokens. It currently has overly permissive access.
   - Modify the permissions of `/home/user/app/config.json` so that ONLY the owner has read and write access, and no other permissions are granted to anyone (group or others).

4. **Integrity Verification Log:**
   Generate a final audit log at `/home/user/audit_log.txt` with exactly three lines in the following format:
   Line 1: The plaintext cracked password.
   Line 2: The exact 3-digit octal file permission of `config.json` (e.g., 755).
   Line 3: The SHA256 checksum of the modified `/home/user/app/login.py` (just the hash, no file path).