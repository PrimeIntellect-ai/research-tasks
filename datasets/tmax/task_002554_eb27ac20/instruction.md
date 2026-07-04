You have been hired as a security auditor to remediate a vulnerable file upload handler and enforce new security policies on a server. 

First, examine the image located at `/app/policy.png`. This image contains a printed policy document detailing specific Content Security Policy (CSP) directives and SSH hardening parameters (specifically, the required `AllowUsers` and `PermitRootLogin` settings). You must extract these exact rules using OCR or vision tools.

Second, there is a vulnerable Python script at `/home/user/upload_handler.py`. It decodes base64 payloads and writes them to a designated directory, but it is susceptible to a path traversal vulnerability (CWE-22) allowing an attacker to write outside the intended directory. 

Your task is to write a repaired version of this script at `/home/user/upload_handler_fixed.py`. The new script must:
1. Accept the exact same command-line arguments as the original (`python /home/user/upload_handler_fixed.py <base64_filename> <base64_payload>`).
2. Decode the payload and write it to `/home/user/uploads/` exactly as the original does for valid filenames.
3. Prevent path traversal. If a path traversal attempt is detected in the decoded filename (e.g., using `../` or `/`), the script must print exactly "CWE-22 DETECTED" to standard output and exit with code 1.
4. Prepend the CSP directives extracted from the image as a comment at the very top of the script (format: `# CSP: <extracted_csp_string>`).
5. Create a shell script at `/home/user/apply_ssh_hardening.sh` that appends the SSH hardening rules extracted from the image to `/etc/ssh/sshd_config` (assume the script will be run by a user with proper permissions later, you just need to create the script).

Ensure your fixed Python script's behavior is bit-exact equivalent to the intended safe behavior. An automated fuzzer will test your `/home/user/upload_handler_fixed.py` against a reference oracle with thousands of random base64 filenames and payloads to ensure it correctly handles valid inputs and rejects malicious ones.