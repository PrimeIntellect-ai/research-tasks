You are an incident responder investigating a security issue in a Python web application. Users have reported being redirected to malicious domains immediately after logging in.

You have been provided with the current production application files in `/home/user/webapp/` and a cryptographic integrity file from the last known-good deployment in `/home/user/backup/hashes.txt`.

Perform the following steps:
1. **File Integrity Verification:** Use the provided SHA256 checksum file (`/home/user/backup/hashes.txt`) to identify which file in `/home/user/webapp/` has been modified since the last deployment. 
2. **CWE Identification:** Analyze the modified Python file to identify the vulnerability causing the malicious redirects. Determine the exact CWE (Common Weakness Enumeration) ID that applies to this vulnerability (e.g., CWE-79, CWE-89, etc.).
3. **Investigation Report:** Create a file at `/home/user/report.txt`. 
   - The first line must contain the exact absolute path of the modified file (e.g., `/home/user/webapp/example.py`).
   - The second line must contain the CWE ID of the vulnerability you identified, formatted exactly as `CWE-XXX` (where XXX is the number).
4. **Remediation:** Modify the vulnerable Python file in `/home/user/webapp/` to fix the vulnerability. Ensure that the `next` redirect parameter is safely validated so that it only permits relative URLs (it must start with a single `/` and must not start with `//` or `http`). If the validation fails, it should default to `/dashboard`.

Ensure all modifications are saved and the report file is precisely formatted.