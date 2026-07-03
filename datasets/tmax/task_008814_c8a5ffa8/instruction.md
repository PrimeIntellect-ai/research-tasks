You are a DevSecOps engineer tasked with securing a legacy Bash CGI-based file upload application and implementing a policy-as-code check. The application is located in `/home/user/app/`.

Your tasks are to audit the application, fix the vulnerabilities, enforce secure file permissions, and write an automated policy checker.

**Phase 1: Code Auditing and Remediation**
1. Review the script located at `/home/user/app/cgi-bin/upload.sh`. This script handles file uploads but is susceptible to a serious vulnerability where an attacker can write files outside the intended upload directory.
2. Identify the specific CWE (Common Weakness Enumeration) ID for this vulnerability (e.g., CWE-79, CWE-89, etc.).
3. Modify `/home/user/app/cgi-bin/upload.sh`. On exactly line 2, insert a comment specifying the CWE in this format: `# VULNERABILITY: CWE-XX` (replace XX with the actual number).
4. Fix the vulnerability in the script. Ensure that the extracted `FILENAME` variable is sanitized so that all directory path components are stripped out, leaving only the base filename. You must implement this using standard Bash utilities (like `basename`) or parameter expansion.

**Phase 2: File Permission and Access Control**
The upload directory and its contents currently have overly permissive access rights.
1. Change the permissions of the directory `/home/user/app/uploads` so that it is strictly readable, writable, and executable ONLY by the file owner (the `user` account).
2. Change the permissions of all existing files inside `/home/user/app/uploads/` so they are readable and writable ONLY by the file owner, and NOT executable by anyone.

**Phase 3: Policy-as-Code Automation**
You need to enforce these rules systematically. Write a Bash script at `/home/user/check_policy.sh` that acts as a security policy auditor.
1. The script must be executable (`chmod +x`).
2. When executed, the script must perform the following checks:
   - Verify if the string `# VULNERABILITY: CWE-22` is present in `/home/user/app/cgi-bin/upload.sh`.
   - Verify if there is a service currently listening on TCP port 8080 (the local web service).
   - Verify if the directory `/home/user/app/uploads` has exactly the octal permission `700`.
3. The script must output its findings in strict JSON format to `/home/user/policy_status.json`. The JSON must have exactly this structure:
```json
{
  "cwe_identified": true,
  "port_8080_active": true,
  "uploads_dir_secure": true
}
```
(Replace the boolean values with the actual results of your script's checks).

Ensure your `check_policy.sh` script works completely independently using standard bash commands (`grep`, `ss` or `netstat`, `stat`, etc.) and does not require manual intervention.