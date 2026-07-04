You are an incident responder investigating a compromised server. The system administrators have provided you with a snapshot of the server's SSH configuration and a recent log file that may contain accidentally leaked credentials.

Your task is to analyze these files, identify SSH vulnerabilities, and redact any leaked sensitive data before the logs are sent to an external forensics team.

The files are located in `/home/user/incident_data/`:
1. `/home/user/incident_data/sshd_config`
2. `/home/user/incident_data/server_logs.txt`

Perform the following actions:

**1. SSH Vulnerability Scanning:**
Analyze the `sshd_config` file for weak settings. Specifically, look for any active (uncommented) lines that explicitly allow `PermitRootLogin yes`, `PasswordAuthentication yes`, or `PermitEmptyPasswords yes`.
Extract these exact vulnerable lines (preserving their original spacing/indentation) and save them to `/home/user/ssh_vuln_report.txt`.

**2. Sensitive Data Redaction:**
The `server_logs.txt` file contains an accidental dump of an SSH private key. 
You must create a new file at `/home/user/redacted_logs.txt` that is identical to `server_logs.txt`, except the entire private key block (everything from the line containing `-----BEGIN` to the line containing `-----END`, inclusive) must be replaced with the single exact string `[REDACTED_KEY]`.

Both files `/home/user/ssh_vuln_report.txt` and `/home/user/redacted_logs.txt` must be created with the correct formats. You may use any combination of shell commands, bash scripts, or a script in a language of your choice (like Python) to accomplish this.