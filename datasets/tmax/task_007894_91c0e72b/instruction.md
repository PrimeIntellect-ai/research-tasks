You are a red-team operator simulating an attack against a target web server. As part of your engagement, you have captured some local configuration files, logs, and a certificate chain. You need to perform a multi-stage analysis and data processing task using Bash to prepare for the next phase of your operation.

Complete the following objectives:

1. **Sensitive Data Redaction:** 
   You captured an access log located at `/home/user/access.log`. It contains sensitive session identifiers in the format `session_id=A1B2C3D4...`. 
   Write a Bash script at `/home/user/redact_logs.sh` that reads `/home/user/access.log` and writes the output to `/home/user/redacted.log`. The script must replace the actual token value (which consists of alphanumeric characters) with the exact string `[REDACTED]`. E.g., `session_id=1928ab` becomes `session_id=[REDACTED]`.

2. **Privilege Escalation Auditing:**
   The server has a cron job that runs a local script `/home/user/check_status.sh` as a privileged user. Audit this Bash script to find the line number containing a command injection vulnerability (which allows arbitrary shell commands to be appended to a variable).
   Save just the integer line number of the vulnerable command into `/home/user/vuln_line.txt`.

3. **Certificate Chain Validation:**
   The directory `/home/user/certs/` contains three certificates: `root.crt`, `intermediate.crt`, and `server.crt`. The certificate chain is supposed to be `root -> intermediate -> server`. However, one of the non-root certificates is invalid (e.g., expired, wrong issuer, or corrupted signature) and breaks the chain.
   Identify which certificate file is invalid or fails verification against the chain. Write the exact filename (e.g., `server.crt` or `intermediate.crt`) to `/home/user/invalid_cert.txt`.

4. **Evasion Payload Generation:**
   The target web server has an open redirect vulnerability at `https://target.local/login?next=`. A naive web application firewall (WAF) blocks the payload if the `next` parameter starts with `http://`, `https://`, or `javascript:`.
   Craft an evasion payload that bypasses these specific schema filters using a protocol-relative URL to redirect the victim to `evil.com`.
   Save your exact URL-decoded payload string (just the payload to be supplied to the `next` parameter) to `/home/user/payload.txt`.