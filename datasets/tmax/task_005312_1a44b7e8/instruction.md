You are a security engineer assigned to audit and secure a legacy credential rotation system, and then perform a credential rotation. 

The system uses a Bash script located at `/home/user/cred_rotator.sh` to process incoming credential updates. The script reads ".job" files from `/home/user/incoming_uploads/`. Each ".job" file contains a target filename and base64-encoded file contents, separated by a colon (`:`). The script decodes the payload and writes it to the `/home/user/certs/` directory.

However, the script is susceptible to a path traversal vulnerability.

Your task consists of the following phases:

**Phase 1: Exploit the Vulnerability (Proof of Concept)**
1. Analyze `/home/user/cred_rotator.sh` to understand how it extracts the filename and data.
2. Craft a malicious job file located at `/home/user/incoming_uploads/exploit.job`.
3. This payload must exploit the path traversal vulnerability so that when `/home/user/cred_rotator.sh` is run, it writes the exact string `ROTATED_SECRET_999` (with a trailing newline) to the file `/home/user/auth_keys/master_token.txt`, overwriting the old token.
4. Execute `/home/user/cred_rotator.sh` to deploy your exploit and rotate the token.

**Phase 2: Remediate the Vulnerability**
1. Create a patched version of the script and save it to `/home/user/cred_rotator_secure.sh`.
2. The patched script must use Bash pattern matching or standard utilities (like `sed` or `tr`) to sanitize the extracted filename before writing the decoded file. Specifically, you must strip all period (`.`) and slash (`/`) characters from the filename variable so that a payload attempting path traversal will be safely written into the `/home/user/certs/` directory instead of escaping it.
3. Ensure `/home/user/cred_rotator_secure.sh` has executable permissions (`chmod +x`).

**Phase 3: File Integrity Verification**
1. To confirm the rotation was successful, calculate the SHA256 checksum of the newly overwritten `/home/user/auth_keys/master_token.txt`.
2. Save the checksum output to `/home/user/token_checksum.txt`. The format must exactly match the default output of `sha256sum` (e.g., `<hash>  /home/user/auth_keys/master_token.txt`).

**Constraints:**
- Do not use `sudo` or modify system-wide configurations. All work must be done within `/home/user/`.
- The format of the `.job` files is exactly `<filename>:<base64_data>`.
- The fixed script must retain the core functionality of reading `.job` files, decoding the base64 payload, and saving them to the certs directory, just with proper filename sanitization.