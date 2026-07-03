You are acting as a network security engineer. You have been reviewing traffic logs on a server and suspect it has been compromised via a custom file upload script.

Here is the situation:
- The server processes uploads using a script located at `/home/user/upload_handler.sh`.
- You have a simplified HTTP traffic capture log located at `/home/user/network_capture.log`.
- You suspect the attacker used a path traversal vulnerability to write an unauthorized SSH key, and also uploaded a password-protected malicious archive.

Your objectives are to investigate, remediate the vulnerability, and extract the malicious payload for analysis:

1. **Vulnerability Remediation**: Analyze `/home/user/upload_handler.sh`. It currently accepts a `FILENAME` environment variable and writes standard input to `/home/user/uploads/$FILENAME`. Modify `/home/user/upload_handler.sh` to securely handle file names by stripping any directory paths. If an attacker passes `FILENAME="../../../home/user/test.txt"`, the script MUST write the file strictly to `/home/user/uploads/test.txt` (i.e., apply `basename` to the filename).

2. **SSH Hardening & Key Management**: The attacker successfully placed an SSH key into `/home/user/.ssh/authorized_keys` using the path traversal exploit. Inspect the `network_capture.log` to identify the attacker's key, and carefully remove ONLY the attacker's key from `/home/user/.ssh/authorized_keys`. Leave any existing legitimate keys intact.

3. **Payload Extraction & Password Cracking**: 
   - The `network_capture.log` contains a second malicious request with a base64-encoded ZIP file payload.
   - Extract this base64 payload, decode it, and save it to `/home/user/extracted_payload.zip`.
   - The ZIP file is password protected. Write a Bash script at `/home/user/crack.sh` to brute-force the ZIP password. You know the password is exactly **3 lowercase English letters** (e.g., `aaa` to `zzz`).
   - Use your script to extract the contents (`malware.sh`) to `/home/user/malware.sh`.

4. **File Integrity Verification**: 
   - Compute the SHA-256 hash of the extracted `/home/user/malware.sh`.
   - Save ONLY the 64-character hex hash into `/home/user/malware_hash.txt` (do not include the filename or trailing spaces in the file).

Ensure all requested files are placed exactly at the specified paths. You may use standard Linux utilities available (e.g., `unzip`, `base64`, `sha256sum`, bash loops).