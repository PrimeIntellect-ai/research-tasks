You are acting as a security auditor investigating a compromised web server environment. A rudimentary file upload handler written in Bash CGI is suspected to be vulnerable to a path traversal attack. The attacker may have used this to escalate privileges or establish persistence.

Your task is to investigate the logs, identify the attack, remediate the vulnerabilities, and produce an audit report.

Perform the following steps:

1. **Log Analysis & Correlation:**
   Examine the web server access logs located at `/home/user/webapp/logs/access.log`. Identify the IP address of the attacker who successfully exploited a path traversal vulnerability (HTTP status 200) to write outside the intended upload directory. 
   Determine the exact absolute path of the system file that the attacker targeted and modified using this exploit.

2. **SSH Hardening & Key Management:**
   The attacker used the traversal vulnerability to inject a rogue SSH key into the system. Inspect `/home/user/.ssh/authorized_keys`. The only legitimate key belongs to the user with the comment `admin@corp.local`. Identify the attacker's injected key, record its comment, and remove the attacker's key from the `authorized_keys` file so the system is secure.

3. **Permission Remediation:**
   The upload handler script located at `/home/user/webapp/cgi-bin/upload.sh` has excessively permissive file permissions, contributing to the system's risk. Fix its permissions so that it is readable and executable by everyone, but writable *only* by the owner (standard 755 permissions).

4. **Audit Report:**
   Generate a JSON report of your findings. Save this report to `/home/user/audit_report.json`. The file must exactly match this format:
   ```json
   {
     "attacker_ip": "<IP_ADDRESS>",
     "compromised_file": "<ABSOLUTE_PATH_OF_TARGETED_FILE>",
     "removed_ssh_key_comment": "<COMMENT_AT_END_OF_ATTACKER_KEY>"
   }
   ```

Complete all remediation steps and ensure the `audit_report.json` file is correctly formatted and accurate.