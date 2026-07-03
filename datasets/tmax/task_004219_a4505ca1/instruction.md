You are acting as a digital forensics analyst investigating a compromised Linux host. You have been provided with a localized dump of the system configuration and a web server access log. Your objective is to audit the system dump for the privilege escalation vector the attacker used, inspect the HTTP logs to identify data exfiltration via headers/cookies, and safely redact the sensitive data from the logs using Python.

**Environment details:**
All your investigation files are located in `/home/user/investigation/`.
1. `/home/user/investigation/system_dump/`: A directory containing a partial file system dump from the compromised host (e.g., `etc/sudoers`, `etc/cron.d/`, `opt/`).
2. `/home/user/investigation/http_logs.json`: A JSON file containing logged HTTP requests, including headers, cookies, and source IPs.

**Your objectives:**

1. **Privilege Escalation Auditing:**
   Analyze the files in `/home/user/investigation/system_dump/`. Identify the script or binary that the attacker used to escalate privileges. The vulnerability is a misconfiguration allowing arbitrary execution without a password as root via `sudo`. 

2. **HTTP Header and Cookie Inspection:**
   The attacker exfiltrated US Social Security Numbers (format: `XXX-XX-XXXX`, where X is a digit) by embedding them inside HTTP headers or cookies in the web traffic. Identify the source IP address of the attacker performing this exfiltration.

3. **Sensitive Data Redaction (Python):**
   Write a Python script at `/home/user/redact.py` that reads `/home/user/investigation/http_logs.json`. The script must:
   - Identify any SSNs (`XXX-XX-XXXX`) hidden within the HTTP headers or cookies of the JSON objects.
   - Replace every digit of the SSN with the letter `X`, preserving the dashes (i.e., every SSN becomes `XXX-XX-XXXX`).
   - Write the sanitized logs to a new file at `/home/user/investigation/http_logs_redacted.json`. The structure must be identical to the original file, just with the SSNs redacted.

4. **Forensic Summary:**
   Create a JSON report at `/home/user/forensic_summary.json` with the following precise keys:
   - `"privesc_vector"`: The absolute path of the misconfigured file inside the dump that allowed the privilege escalation (e.g., `"/home/user/investigation/system_dump/opt/scripts/backup.sh"`).
   - `"malicious_ip"`: The IP address of the attacker exfiltrating the SSNs.
   - `"exfiltrated_records_count"`: The total number of HTTP log entries (JSON objects) that contained at least one SSN before redaction.

Ensure your Python script runs successfully and generates the required output files. Both `/home/user/investigation/http_logs_redacted.json` and `/home/user/forensic_summary.json` will be verified programmatically.