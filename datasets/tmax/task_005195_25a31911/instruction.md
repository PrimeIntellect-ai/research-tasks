You are acting as a Security Auditor for a company's newly deployed internal service. You need to verify the application's SSL certificates, audit its access logs for intrusion attempts while redacting sensitive data, and secure the log directory's file permissions.

Your objective is to write and execute a Python script at `/home/user/auditor.py` that performs the following tasks and outputs a JSON report to `/home/user/audit_report.json`.

### Requirements for `/home/user/auditor.py`:

**1. Certificate Chain Validation**
The application uses certificates located in `/home/user/app/certs/`.
*   Read the Certificate Authority (CA) certificate at `/home/user/app/certs/ca.pem`.
*   Read the server certificate at `/home/user/app/certs/server.pem`.
*   Verify that `server.pem` is validly signed by `ca.pem` and is currently within its validity period.
*   Your script must output a boolean value for this check in the final report. You may use the `cryptography` Python library.

**2. Intrusion Detection & Sensitive Data Redaction**
The application writes logs to `/home/user/app/logs/access.log`.
*   Scan this file line-by-line for intrusion attempts. An intrusion attempt is defined as any log line matching the following case-insensitive substrings:
    *   `UNION SELECT`
    *   `etc/passwd`
    *   `../`
*   Before recording the intrusion line, you must **redact** any AWS-style access keys. Find any occurrence of the regex pattern `AKIA[0-9A-Z]{16}` and replace the entire key with the string `[REDACTED]`.
*   Collect all redacted intrusion lines into a list.

**3. Permissions Audit**
As an auditor, you must ensure logs are not world-readable.
*   Scan all files in the directory `/home/user/app/logs/`.
*   Identify any file that grants any permissions to "others" (e.g., world-readable, world-writable, or world-executable).
*   Change the permissions of those files to `640` (Owner: Read/Write, Group: Read, Others: None).
*   Record the absolute paths of the files whose permissions were modified.

**4. Output Format**
Your script must output a strictly formatted JSON file at `/home/user/audit_report.json` with the following structure:
```json
{
  "cert_valid": true,
  "intrusions": [
    "192.168.1.50 - GET /api/data?key=[REDACTED]&query=UNION SELECT * FROM users HTTP/1.1",
    "10.0.0.2 - GET /download?file=../../../../etc/passwd HTTP/1.1"
  ],
  "fixed_files": [
    "/home/user/app/logs/access.log"
  ]
}
```

Ensure your script handles dependencies (if you need any libraries like `cryptography`, you may install them via pip in the terminal before running your script). Write the script, execute it, and ensure `/home/user/audit_report.json` is generated successfully.