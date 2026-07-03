You are a penetration tester tasked with analyzing a recovered application backup from a compromised server. The backup is located in `/home/user/app_backup/`. You must analyze the files, extract sensitive information, audit the code, and remediate data leaks. 

Write a Python script (or execute shell commands) to complete the following objectives, and compile your final findings into a JSON report at `/home/user/report.json`.

**Objective 1: Password Cracking**
The file `/home/user/app_backup/admin_hash.txt` contains the SHA-256 hash of the administrator's password. A dictionary of potential passwords is provided at `/home/user/wordlist.txt`. Crack the password.

**Objective 2: Certificate Chain Validation**
The directory `/home/user/app_backup/certs/` contains a custom TLS certificate chain: `root.pem`, `intermediate.pem`, and `leaf.pem`. Write Python code using the `cryptography` or `OpenSSL` library to validate the certificate chain to determine if `leaf.pem` is successfully verified by the root (via the intermediate). Note: check for valid signatures and expiration. 

**Objective 3: Code Auditing**
Analyze the Python script `/home/user/app_backup/server.py`. Identify the primary vulnerability present in the `handle_ping` function. You must identify the most specific MITRE CWE identifier (e.g., "CWE-79") for this vulnerability.

**Objective 4: Sensitive Data Redaction**
The file `/home/user/app_backup/app.log` contains application logs, but it has leaked customer credit card numbers. Credit card numbers in this log follow the exact format `XXXX-XXXX-XXXX-XXXX` (where X is a digit). 
Create a new file `/home/user/app_backup/app_redacted.log` where every credit card number is replaced with the exact string `[REDACTED]`. Count how many lines in the log file were modified.

**Final Deliverable**
Create a file at `/home/user/report.json` with the exact following schema:
```json
{
  "admin_password": "the_cracked_plaintext_password",
  "cert_valid": true_or_false,
  "cwe_vulnerability": "CWE-XXX",
  "redacted_log_lines_count": integer_number_of_modified_lines
}
```