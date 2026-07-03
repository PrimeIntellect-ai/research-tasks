You are acting as a security engineer responding to a recent security incident. A legacy Bash-based file processing system has been compromised due to a path traversal vulnerability. Your job is to audit the code, clean up compromised files, rotate the authentication tokens, and block the attacker's IP.

You must complete the following four phases entirely using Bash and standard Linux tools.

**Phase 1: Code Auditing and Patching**
Review the script located at `/home/user/upload_handler.sh`. It currently accepts a filename and copies it to the uploads directory. It is vulnerable to path traversal.
1. Modify `/home/user/upload_handler.sh` to explicitly reject any `FILENAME` that contains a forward slash (`/`) or the string `..`. If a malicious filename is detected, the script should output "Invalid filename" and exit with status code 1.
2. Create an audit log file at `/home/user/audit.log`. Write exactly the string `CWE-22 detected and patched` into this file.

**Phase 2: File Integrity Verification**
The attacker may have altered files or dropped unauthorized files in the `/home/user/uploads/` directory.
1. You have been provided a known-good hash file at `/home/user/hashes.txt` (format: `sha256sum` output).
2. Compare every file currently in `/home/user/uploads/` against `hashes.txt`.
3. If a file's hash does not match, or if a file is not listed in `hashes.txt` at all, move it to `/home/user/quarantine/`. Do not delete the files. Ensure `/home/user/quarantine/` exists.

**Phase 3: Token Generation and Rotation**
The attacker stole the old access tokens. You must rotate them.
1. Generate exactly 5 new secure, random 32-character alphanumeric tokens (A-Z, a-z, 0-9).
2. Save these plain-text tokens, one per line, to `/home/user/new_tokens_secret.txt`.
3. Compute the SHA256 hash of each new token. Overwrite `/home/user/valid_tokens.txt` with these new hashes (format: standard `sha256sum` output, e.g., `<hash>  -`).

**Phase 4: Network Policy Configuration**
The attacker's IP address was identified as `198.51.100.42`. 
1. Open the application firewall config file at `/home/user/network_rules.conf`.
2. Append a new rule to the top or bottom of the file to block this IP. The exact format must be: `DENY 198.51.100.42`.

Ensure all files have the exact names and paths specified above.