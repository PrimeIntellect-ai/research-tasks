You are acting as a Compliance Security Analyst. A web server was recently compromised. The attacker exploited an open redirect vulnerability combined with an XSS payload to steal session tokens, and subsequently escalated privileges on the host system.

Your task is to analyze the server logs and system configuration backups, sanitize the data for compliance, and generate a final audit report.

**Step 1: Log Analysis and Decoding**
You have been provided with an access log at `/home/user/server_logs.log`. The logs contain HTTP GET requests. 
Some requests target a login flow with a `redirect` query parameter. 
The attacker obfuscated their XSS payloads inside this `redirect` parameter using a combination of URL encoding and Base64 encoding (e.g., `?redirect=base64_encoded_url_encoded_string`).
- Find all log entries where the `redirect` parameter contains a decoded payload that includes the string `<script>` or `javascript:`.
- Extract the source IP addresses of these malicious requests.
- Extract the fully decoded payloads.

**Step 2: Sensitive Data Redaction**
Compliance rules dictate that no PII or active session data can remain in the audit logs.
Create a new file at `/home/user/redacted_logs.log` which contains the exact contents of `/home/user/server_logs.log`, but with the following redactions:
- Any US Social Security Number (format: `XXX-XX-XXXX`) must be replaced exactly with `[REDACTED_SSN]`.
- Any Bearer token (format: `Bearer [A-Za-z0-9+/=]{16,}`) must be replaced exactly with `Bearer [REDACTED_TOKEN]`.

**Step 3: Privilege Escalation Auditing**
The attacker managed to escalate to `root`. A backup of the system's configuration files is located in the directory `/home/user/system_configs/`.
Audit the configuration files in this directory to find the specific misconfiguration that allows a low-privileged user to escalate privileges to root without a password. 
Look for common Linux local privilege escalation vectors (e.g., insecure sudoers rules, writable cron jobs running as root). Identify the exact absolute file path of the configuration file inside `/home/user/system_configs/` that contains the vulnerability.

**Step 4: Generate the Audit Report**
Create a final JSON report at `/home/user/compliance_audit.json` with the following precise structure:
```json
{
  "malicious_ips": [
    "IP1",
    "IP2"
  ],
  "decoded_xss_payloads": [
    "payload1",
    "payload2"
  ],
  "privesc_vuln_file": "/home/user/system_configs/path/to/file",
  "redacted_log_lines_count": 0 
}
```
*Note for `redacted_log_lines_count`: Count the number of lines in `/home/user/redacted_logs.log` that were modified (i.e., contained a redaction).*

You may use any programming language or shell utilities available on the system to complete this task.