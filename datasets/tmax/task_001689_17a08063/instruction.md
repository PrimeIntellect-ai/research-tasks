You are a DevSecOps engineer enforcing policy as code for a system that has recently been audited. An audit log file has been placed at `/home/user/syslog.txt`. It contains system events, SSH login attempts, and command logs.

A recent vulnerability scan indicated two issues:
1. Brute-force SSH attempts are occurring, and the IPs need to be identified for firewall blocking.
2. An internal script accidentally dumped OpenSSH private keys into the system logs, which poses a severe security risk.

Your task is to remediate these issues using standard bash utilities.

Perform the following operations:
1. **Intrusion Detection Pattern Matching**: Find all IP addresses associated with a "Failed password" event in `/home/user/syslog.txt`. Extract only the IPv4 addresses, sort them, remove duplicates, and write them to `/home/user/blocked_ips.txt` (one IP per line).
2. **Sensitive Data Redaction**: Parse `/home/user/syslog.txt` and redact any leaked OpenSSH private keys. You must find any block of text starting with `-----BEGIN OPENSSH PRIVATE KEY-----` and ending with `-----END OPENSSH PRIVATE KEY-----` (inclusive of these marker lines) and replace the entire multi-line block with a single line containing exactly: `[REDACTED]`. Save this sanitized log to `/home/user/syslog_redacted.txt`. Do not alter any other lines in the file.

Constraints:
- Only use standard shell utilities (e.g., `grep`, `awk`, `sed`, `sort`, `uniq`).
- Do not modify the original `/home/user/syslog.txt`.