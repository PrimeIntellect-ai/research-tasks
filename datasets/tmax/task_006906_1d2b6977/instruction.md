You are acting as a security auditor for a small web application. You have been provided access to the application source code and some system files. Your goal is to identify unauthorized modifications, locate specific vulnerabilities, and ensure secure configurations.

Please perform the following tasks:

1. **File Integrity Verification:**
   The application files are located in `/home/user/webapp/`. There is a checksum file at `/home/user/webapp/checksums.txt` containing the expected SHA-256 hashes of the Python files in that directory. Identify the single `.py` file that has been modified (its current hash does not match the one in `checksums.txt`).

2. **Vulnerability Analysis - Command Injection:**
   Inspect the modified file you identified in step 1. Find the exact line number where a Command Injection vulnerability is present (where unsanitized input is passed directly to a shell command execution function).

3. **Vulnerability Analysis - XSS:**
   Inspect the file `/home/user/webapp/views.py`. Find the exact line number of a Cross-Site Scripting (XSS) vulnerability, specifically where unsanitized user input is concatenated into an HTML string.

4. **SSH Hardening:**
   Check the user's SSH directory at `/home/user/.ssh/`. Ensure that the private key file `id_rsa` has the appropriately restrictive permissions for a private key. Modify its permissions if they are currently insecure.

5. **Reporting:**
   Create a JSON report file at `/home/user/audit.json` with your findings. The JSON file must have the following exact keys and format:
   ```json
   {
     "modified_file": "<filename.py>",
     "injection_line_number": <integer>,
     "xss_line_number": <integer>,
     "ssh_permissions_fixed": true
   }
   ```
   (Replace the placeholders with your actual findings. Set `ssh_permissions_fixed` to `true` if you corrected the permissions).